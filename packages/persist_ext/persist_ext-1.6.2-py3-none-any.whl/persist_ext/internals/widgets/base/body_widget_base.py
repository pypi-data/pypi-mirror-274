import json

import traittypes
from abc import ABC, abstractmethod
from copy import deepcopy
from threading import Thread


import traitlets
from persist_ext.internals.data.idfy import ID_COLUMN, idfy_dataframe
from persist_ext.internals.widgets.base.widget_with_trrack import WidgetWithTrrack
from persist_ext.internals.widgets.interactions.annotation import (
    ANNOTATE_COLUMN_NAME,
    NO_ANNOTATION,
    create_annotation_string,
)
from persist_ext.internals.widgets.interactions.selection import (
    SELECTED_COLUMN_BRUSH,
    SELECTED_COLUMN_INTENT,
    selected,
)


def is_int_or_float(v):
    if isinstance(v, int) or isinstance(v, float):
        return True
    if isinstance(v, str):
        try:
            if "." in v:
                float(v)
            else:
                int(v)
            return True
        except:  # noqa
            return False
    else:
        return False


def is_str(v):
    return isinstance(v, str)


class _AbstractWidgetWithTrrack(type(WidgetWithTrrack), type(ABC)):
    pass


class BodyWidgetBase(WidgetWithTrrack, ABC, metaclass=_AbstractWidgetWithTrrack):
    # Base dataframe never changes
    _persistent_data = traittypes.DataFrame()

    # Backing dataframe for the view
    data = traittypes.DataFrame()

    is_applying = traitlets.Bool(default_value=False).tag(sync=True)

    def __init__(self, data, *args, **kwargs):
        if type(self) is BodyWidgetBase:
            raise NotImplementedError("Cannot create instance of this base class")

        # create copy of the data so that it delinks from the chart
        data = data.copy(deep=True)

        # add id column if not present
        if ID_COLUMN not in data:
            data = idfy_dataframe(data)

        # add selected column and set it to False
        data[SELECTED_COLUMN_BRUSH] = False

        # Add selected intent column and set it to False
        data[SELECTED_COLUMN_INTENT] = False

        # Add an annotation column and set it to NO_ANNOTATION
        data[ANNOTATE_COLUMN_NAME] = NO_ANNOTATION

        data = data.convert_dtypes()
        self._cached_apply_record = dict()

        super(BodyWidgetBase, self).__init__(
            data=data, _persistent_data=data.copy(deep=True), *args, **kwargs
        )

    @traitlets.observe("data")
    def _handle_data_update(self, change):
        """
        Do the following on data change:
        - set `df_columns` to columns of the new dataset
        - set `df_non_meta_columns` by filtering out `df_meta_columns`
        - set `df_values` to jsonified pandas dataframe

        """
        new_data = change.new

        with self.hold_sync():
            # Set columns
            columns = list(new_data.columns)
            self.df_columns = columns
            self.df_non_meta_columns = list(
                filter(lambda x: x not in self.df_meta_columns, columns)
            )
            self.df_numeric_columns = list(
                new_data[self.df_non_meta_columns]
                .select_dtypes(include="number")
                .columns
            )
            self.df_column_dtypes = json.loads(
                new_data.dtypes.to_json(default_handler=str)
            )

            # Set default sorts
            if len(self.df_column_sort_status) == 0:
                new_data = new_data.sort_values(
                    by=self.df_id_column_name,
                    ascending=True,
                    key=(lambda x: x.astype("Int64")),
                )

            # Set selections
            selected_data = new_data[[self.df_id_column_name]]

            selected_data.loc[:, ["SELECTED"]] = (
                new_data[SELECTED_COLUMN_BRUSH] | new_data[SELECTED_COLUMN_INTENT]
            )

            selected_data = (
                selected_data[selected_data["SELECTED"]]
                .set_index(self.df_id_column_name)["SELECTED"]
                .to_dict()
            )
            self.df_row_selection_status = selected_data

            self.df_has_selections = len(self.df_row_selection_status) > 0

            df_possible_dtypes = self.df_possible_dtypes

            for col_name in new_data.select_dtypes(include=["string"]):
                if new_data[col_name].apply(is_int_or_float).all():
                    df_possible_dtypes["string"] = ["string", "Int64", "Float64"]

            self.df_possible_dtypes = df_possible_dtypes

            # Set values
            self.df_values = json.loads(new_data.to_json(orient="records"))

    def _finish(self):
        pass

    ## Interactions
    @traitlets.observe("interactions")
    def _on_interaction_change(self, change):
        interactions = change.new
        self._interaction_change(interactions)
        self._finish()

    def _interaction_change(self, interactions):
        # Set is_apply flag to true
        self.is_applying = True

        # copy all vars to update
        copied_var_tuple = self._copy_vars()

        # Apply interactions
        copied_var_tuple = self._apply_interactions(interactions, *copied_var_tuple)

        # Replace traitlets with copies by holding sync
        with self.hold_sync():
            if len(interactions) < 2:
                self.df_column_sort_status = []
            self._update_copies(*copied_var_tuple)
            self.is_applying = False

    # Loop over interaction and update the copies
    def _apply_interactions(self, interactions, *copied_var_tuple):
        # Set cache hit status to None
        last_cache_hit_id = None
        threads = []

        # loop over interactions
        for interaction in interactions:
            id = interaction["id"]
            # check if interaction is cached
            if id in self._cached_apply_record:
                # if yes then set the last_cache_hit_id
                last_cache_hit_id = id
            else:
                # last interaction was  cached
                if last_cache_hit_id is not None:
                    # Load the cached values
                    copied_var_tuple = self._from_cache(
                        *self._cached_apply_record[last_cache_hit_id]
                    )
                    # reset last_cache_hit_id
                    last_cache_hit_id = None

                # Get type and apply
                _type = interaction["type"]
                fn_name = f"_apply_{_type}"
                if hasattr(self, fn_name):
                    fn = getattr(self, fn_name)
                    copied_var_tuple = fn(interaction, *copied_var_tuple)

                    # Update the cache with interaction id in thread
                    def __update(id, vars_to_copy):
                        self._cached_apply_record[id] = vars_to_copy

                    # __update(id, self._to_cache(*copied_var_tuple))

                    thread = Thread(
                        target=__update, args=(id, self._to_cache(*copied_var_tuple))
                    )
                    thread.start()
                    threads.append(thread)
                else:
                    raise ValueError(f"Method {fn_name} not implemented")

        # If last hit is set, retrieve it and return
        if last_cache_hit_id is not None:
            copied_var_tuple = self._from_cache(
                *self._cached_apply_record[last_cache_hit_id]
            )

        for t in threads:
            t.join()

        return copied_var_tuple

    @abstractmethod
    def _to_cache(self, *args):
        pass

    @abstractmethod
    def _from_cache(self, *args):
        pass

    def _default_cache_to_from(self, *args):
        return deepcopy(args)

    @abstractmethod
    def _get_data(self, *args):
        pass

    @abstractmethod
    def _copy_vars(self):
        pass

    @abstractmethod
    def _update_copies(self, *args):
        pass

    ##### interaction methods
    # create
    @abstractmethod
    def _apply_create(self, **kwargs):
        pass

    # selection
    @abstractmethod
    def _apply_select(self, **kwargs):
        pass

    @abstractmethod
    def _apply_intent(self, **kwargs):
        pass

    @abstractmethod
    def _clear_selections(self, data):
        pass

    def _clear_selection_data(self, data):
        data[SELECTED_COLUMN_BRUSH] = False
        data[SELECTED_COLUMN_INTENT] = False

        return data

    # filter
    @abstractmethod
    def _apply_filter(self, **kwargs):
        pass

    def _filter_common(self, data, direction):
        if direction == "in":
            data = data[selected(data)]
        else:
            data = data[~selected(data)]

        data = data.reset_index(drop=True)

        return data

    # categorize
    @abstractmethod
    def _apply_categorize(self, **kwargs):
        pass

    def _categorize_common(self, data, categorize_interaction):
        category = categorize_interaction["category"]
        option = categorize_interaction["option"]

        if category not in data:
            data[category] = "_None"

        data.loc[selected(data), category] = option

        return data

    # annotate
    @abstractmethod
    def _apply_annotate(self, **kwargs):
        pass

    def _annotate_common(self, data, annotate_interaction):
        text = annotate_interaction["text"]
        created_on = annotate_interaction["createdOn"]
        annotation_str = create_annotation_string(text, created_on)

        def _append_annotation(val):
            if val == NO_ANNOTATION:
                return annotation_str
            return f"{val} | {annotation_str}"

        data.loc[selected(data), ANNOTATE_COLUMN_NAME] = data.loc[
            selected(data), ANNOTATE_COLUMN_NAME
        ].apply(_append_annotation)

        return data

    # rename
    @abstractmethod
    def _apply_rename_column(self, **kwargs):
        pass

    def _rename_columns_common(self, data, rename_interaction):
        rename_column_map = rename_interaction["renameColumnMap"]

        data = data.rename(columns=rename_column_map)

        return data

    # drop
    @abstractmethod
    def _apply_drop_columns(self, **kwargs):
        pass

    def _drop_columns_common(self, data, columns):
        if len(columns) > 0:
            data = data.drop(columns, axis=1)

        return data

    @abstractmethod
    def _apply_sortby_column(self, **kwargs):
        pass

    @abstractmethod
    def _apply_reorder_column(self, **kwargs):
        pass

    @abstractmethod
    def _apply_edit_cell(self, **kwargs):
        pass

    @abstractmethod
    def _apply_column_type_change(self, **kwargs):
        pass
