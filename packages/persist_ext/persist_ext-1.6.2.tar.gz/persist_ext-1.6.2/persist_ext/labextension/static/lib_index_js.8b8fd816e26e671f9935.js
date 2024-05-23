"use strict";
(self["webpackChunkpersist_ext"] = self["webpackChunkpersist_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/cells/trrackableCell.js":
/*!*************************************!*\
  !*** ./lib/cells/trrackableCell.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ACTIVE_CATEGORY: () => (/* binding */ ACTIVE_CATEGORY),
/* harmony export */   CODE_CELL: () => (/* binding */ CODE_CELL),
/* harmony export */   GENERATED_DATAFRAMES: () => (/* binding */ GENERATED_DATAFRAMES),
/* harmony export */   HAS_PERSIST_OUTPUT: () => (/* binding */ HAS_PERSIST_OUTPUT),
/* harmony export */   TRRACK_GRAPH: () => (/* binding */ TRRACK_GRAPH),
/* harmony export */   TrrackableCell: () => (/* binding */ TrrackableCell),
/* harmony export */   VEGALITE_SPEC: () => (/* binding */ VEGALITE_SPEC)
/* harmony export */ });
/* harmony import */ var _hookstate_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @hookstate/core */ "webpack/sharing/consume/default/@hookstate/core/@hookstate/core?4643");
/* harmony import */ var _hookstate_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_hookstate_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _hookstate_localstored__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @hookstate/localstored */ "webpack/sharing/consume/default/@hookstate/localstored/@hookstate/localstored");
/* harmony import */ var _hookstate_localstored__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_hookstate_localstored__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _hookstate_subscribable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @hookstate/subscribable */ "webpack/sharing/consume/default/@hookstate/subscribable/@hookstate/subscribable");
/* harmony import */ var _hookstate_subscribable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_hookstate_subscribable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _utils_cellStoreEngine__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../utils/cellStoreEngine */ "./lib/utils/cellStoreEngine.js");
/* harmony import */ var _widgets_trrack_manager__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../widgets/trrack/manager */ "./lib/widgets/trrack/manager.js");
/* harmony import */ var _utils_stripImmutableClone__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../utils/stripImmutableClone */ "./lib/utils/stripImmutableClone.js");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);








const CODE_CELL = 'code-cell';
const TRRACK_GRAPH = 'trrack_graph';
const VEGALITE_SPEC = 'vegalite-spec';
const ACTIVE_CATEGORY = 'active-category';
const GENERATED_DATAFRAMES = '__GENERATED_DATAFRAMES__';
const HAS_PERSIST_OUTPUT = '__has_persist_output';
class TrrackableCell extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell {
    constructor(opts) {
        super(opts);
        // Trrack graph
        this.__trrackGraph = null;
        this._trrackManager = null;
        if (!window.Persist.CellMap) {
            throw new Error('Entry point not executed');
        }
        window.Persist.CellMap.set(this.cell_id, this);
        const savedGenRecordString = this.model.getMetadata(GENERATED_DATAFRAMES);
        const savedGenRecord = {};
        savedGenRecordString
            ? JSON.parse((0,_utils_cellStoreEngine__WEBPACK_IMPORTED_MODULE_5__.decompressString)(savedGenRecordString))
            : null;
        this._generatedDataframes = (0,_hookstate_core__WEBPACK_IMPORTED_MODULE_0__.hookstate)(savedGenRecord, (0,_hookstate_core__WEBPACK_IMPORTED_MODULE_0__.extend)((0,_hookstate_subscribable__WEBPACK_IMPORTED_MODULE_2__.subscribable)(), (0,_hookstate_localstored__WEBPACK_IMPORTED_MODULE_1__.localstored)({
            key: GENERATED_DATAFRAMES,
            engine: (0,_utils_cellStoreEngine__WEBPACK_IMPORTED_MODULE_5__.getCellStoreEngine)(this)
        })));
        // const savedString = this.model.getMetadata(TRRACK_GRAPH);
        // const savedGraph: TrrackGraph | null = savedString
        //   ? JSON.parse(decompressString(savedString))
        //   : null;
        //
        // this._trrackGraph = hookstate<TrrackGraph | null, LocalStored>(
        //   savedGraph,
        //   localstored({
        //     key: TRRACK_GRAPH,
        //     engine: getCellStoreEngine(this)
        //   })
        // );
        // add id so that it can be extracted
        this.node.dataset.id = this.cell_id;
        // add the code-cell tag
        this.node.dataset.celltype = CODE_CELL;
        const displayPersistNotice = async (outputModel, _) => {
            await this.ready;
            const node = this.node;
            const footer = node.querySelector('.jp-CellFooter');
            if (outputModel.length !== 0) {
                if (footer) {
                    footer.innerHTML = '';
                }
                return;
            }
            if (this.model.getMetadata(TRRACK_GRAPH)) {
                if (footer) {
                    footer.style.height = 'auto';
                    footer.innerHTML = `
                <div style="height:20px;width:100%;text-align:center">
                This cell is a persist cell. Please run the cell to enable interactive output.
                </div>
                  `;
                }
            }
        };
        this.model.outputs.changed.connect(displayPersistNotice, this);
        displayPersistNotice(this.model.outputs, this);
    }
    get _trrackGraph() {
        if (this.__trrackGraph === null) {
            const savedString = this.model.getMetadata(TRRACK_GRAPH);
            const savedGraph = savedString
                ? JSON.parse((0,_utils_cellStoreEngine__WEBPACK_IMPORTED_MODULE_5__.decompressString)(savedString))
                : null;
            this.__trrackGraph = (0,_hookstate_core__WEBPACK_IMPORTED_MODULE_0__.hookstate)(savedGraph, (0,_hookstate_localstored__WEBPACK_IMPORTED_MODULE_1__.localstored)({
                key: TRRACK_GRAPH,
                engine: (0,_utils_cellStoreEngine__WEBPACK_IMPORTED_MODULE_5__.getCellStoreEngine)(this)
            }));
        }
        return this.__trrackGraph;
    }
    get trrackManager() {
        if (!this._trrackManager) {
            this._trrackManager = _widgets_trrack_manager__WEBPACK_IMPORTED_MODULE_6__.TrrackManager.getInstance(this);
        }
        return this._trrackManager;
    }
    tagAsPersistCell(has = true) {
        this.model.setMetadata(HAS_PERSIST_OUTPUT, has);
    }
    get generatedDataframesState() {
        return this._generatedDataframes;
    }
    get generatedDataframes() {
        return (0,_utils_stripImmutableClone__WEBPACK_IMPORTED_MODULE_7__.stripImmutableCloneJSON)(this._generatedDataframes.get({ noproxy: true }));
    }
    get trrackGraphState() {
        return this._trrackGraph;
    }
    get trrackGraph() {
        return (0,_utils_stripImmutableClone__WEBPACK_IMPORTED_MODULE_7__.stripImmutableClone)(this._trrackGraph.get({ noproxy: true }));
    }
    get cell_id() {
        return this.model.id;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        window.Persist.CellMap.delete(this.cell_id);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
        super.dispose();
    }
}
(function (TrrackableCell) {
    function create(options) {
        return new TrrackableCell(options);
    }
    TrrackableCell.create = create;
    function isTrrackableCell(cell) {
        return cell instanceof TrrackableCell;
    }
    TrrackableCell.isTrrackableCell = isTrrackableCell;
})(TrrackableCell || (TrrackableCell = {}));


/***/ }),

/***/ "./lib/cells/trrackableCellFactory.js":
/*!********************************************!*\
  !*** ./lib/cells/trrackableCellFactory.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TrrackableCellFactory: () => (/* binding */ TrrackableCellFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _trrackableCell__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./trrackableCell */ "./lib/cells/trrackableCell.js");


class TrrackableCellFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    createCodeCell(options) {
        return _trrackableCell__WEBPACK_IMPORTED_MODULE_1__.TrrackableCell.create(options).initializeState();
    }
}


/***/ }),

/***/ "./lib/commands/index.js":
/*!*******************************!*\
  !*** ./lib/commands/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PersistCommandRegistry: () => (/* binding */ PersistCommandRegistry),
/* harmony export */   PersistCommands: () => (/* binding */ PersistCommands)
/* harmony export */ });
/* harmony import */ var _interactions_selection__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../interactions/selection */ "./lib/interactions/selection.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");
/* harmony import */ var _interactions_filter__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../interactions/filter */ "./lib/interactions/filter.js");
/* harmony import */ var _interactions_annotate__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../interactions/annotate */ "./lib/interactions/annotate.js");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _interactions_renameColumn__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../interactions/renameColumn */ "./lib/interactions/renameColumn.js");
/* harmony import */ var _interactions_dropColumn__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../interactions/dropColumn */ "./lib/interactions/dropColumn.js");
/* harmony import */ var _interactions_categorize__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../interactions/categorize */ "./lib/interactions/categorize.js");
/* harmony import */ var _interactions_sortByColumn__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../interactions/sortByColumn */ "./lib/interactions/sortByColumn.js");
/* harmony import */ var _interactions_reorderColumns__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../interactions/reorderColumns */ "./lib/interactions/reorderColumns.js");
/* harmony import */ var _interactions_changeColumnType__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../interactions/changeColumnType */ "./lib/interactions/changeColumnType.js");
/* harmony import */ var _interactions_editCell__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../interactions/editCell */ "./lib/interactions/editCell.js");
/* harmony import */ var _interactions_intentSelection__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../interactions/intentSelection */ "./lib/interactions/intentSelection.js");
/* harmony import */ var _widgets_utils_dataframe__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../widgets/utils/dataframe */ "./lib/widgets/utils/dataframe.js");














var PersistCommands;
(function (PersistCommands) {
    // Reset Trrack
    PersistCommands.resetTrrack = 'persist:trrack:reset';
    // Selections
    PersistCommands.pointSelection = 'persist:selection:point';
    PersistCommands.intervalSelection = 'persist:selection:interval';
    PersistCommands.intentSelection = 'persist:selection:intent';
    PersistCommands.invertSelection = 'persist:selection:invert';
    PersistCommands.clearSelection = 'persist:selection:clear';
    // Categorizey
    PersistCommands.categorize = 'persist:category:assign';
    // Filters
    PersistCommands.filterOut = 'persist:filter:out';
    PersistCommands.filterIn = 'persist:filter:in';
    // Column Ops
    PersistCommands.sortByColumn = 'persist:column:sort';
    PersistCommands.reorderColumns = 'persist:column:order';
    PersistCommands.renameColumns = 'persist:column:rename';
    PersistCommands.dropColumns = 'persist:column:drop';
    PersistCommands.changeColumnDataType = 'persist:column:changetype';
    // Annotation
    PersistCommands.annotate = 'persist:annotate';
    // Edit Value
    PersistCommands.editCell = 'persist:data:edit';
    // Generate
    PersistCommands.createDataframe = 'persist:dataframe:create';
    PersistCommands.copyDataframe = 'persist:dataframe:copy';
    PersistCommands.insertCellWithDataframe = 'persist:dataframe:insert-cell';
    PersistCommands.deleteDataframe = 'persist:dataframe:delete';
})(PersistCommands || (PersistCommands = {}));
class PersistCommandRegistry {
    constructor() {
        this._commandsDisposeMap = new Map();
        this._commands = new _lumino_commands__WEBPACK_IMPORTED_MODULE_0__.CommandRegistry();
        this.addCommand(PersistCommands.resetTrrack, {
            isEnabled(args) {
                const { cell } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
                const { nodes } = cell.trrackManager.trrack.exportObject();
                return Object.keys(nodes).length > 1;
            },
            execute(args) {
                const { cell } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
                cell.trrackManager.reset();
            },
            label: 'Reset Trrack'
        });
        this.addCommand(PersistCommands.pointSelection, _interactions_selection__WEBPACK_IMPORTED_MODULE_2__.selectionCommandOption);
        this.addCommand(PersistCommands.intervalSelection, _interactions_selection__WEBPACK_IMPORTED_MODULE_2__.selectionCommandOption);
        this.addCommand(PersistCommands.intentSelection, _interactions_intentSelection__WEBPACK_IMPORTED_MODULE_3__.intentSelectionCommandOption);
        this.addCommand(PersistCommands.invertSelection, {
            execute() {
                throw new Error('not impl');
            }
        });
        this.addCommand(PersistCommands.clearSelection, {
            execute() {
                throw new Error('not impl');
            }
        });
        this.addCommand(PersistCommands.categorize, _interactions_categorize__WEBPACK_IMPORTED_MODULE_4__.categorizeCommandOption);
        this.addCommand(PersistCommands.filterOut, _interactions_filter__WEBPACK_IMPORTED_MODULE_5__.filterCommandOption);
        this.addCommand(PersistCommands.filterIn, _interactions_filter__WEBPACK_IMPORTED_MODULE_5__.filterCommandOption);
        this.addCommand(PersistCommands.sortByColumn, _interactions_sortByColumn__WEBPACK_IMPORTED_MODULE_6__.sortbyColumnCommandOption);
        this.addCommand(PersistCommands.reorderColumns, _interactions_reorderColumns__WEBPACK_IMPORTED_MODULE_7__.reorderColumnsCommandOption);
        this.addCommand(PersistCommands.renameColumns, _interactions_renameColumn__WEBPACK_IMPORTED_MODULE_8__.renameColumnCommandOption);
        this.addCommand(PersistCommands.dropColumns, _interactions_dropColumn__WEBPACK_IMPORTED_MODULE_9__.dropColumnsCommandOption);
        this.addCommand(PersistCommands.annotate, _interactions_annotate__WEBPACK_IMPORTED_MODULE_10__.annotateCommandOption);
        this.addCommand(PersistCommands.changeColumnDataType, _interactions_changeColumnType__WEBPACK_IMPORTED_MODULE_11__.changeColumnTypeCommandOption);
        this.addCommand(PersistCommands.editCell, _interactions_editCell__WEBPACK_IMPORTED_MODULE_12__.editCellCommandOption);
        this.addCommand(PersistCommands.createDataframe, _widgets_utils_dataframe__WEBPACK_IMPORTED_MODULE_13__.createDataframeCommandOption);
        this.addCommand(PersistCommands.deleteDataframe, _widgets_utils_dataframe__WEBPACK_IMPORTED_MODULE_13__.deleteGeneratedDataframeCommandOption);
        this.addCommand(PersistCommands.copyDataframe, _widgets_utils_dataframe__WEBPACK_IMPORTED_MODULE_13__.copyGeneratedDataframeCommandOption);
        this.addCommand(PersistCommands.insertCellWithDataframe, _widgets_utils_dataframe__WEBPACK_IMPORTED_MODULE_13__.insertCellWithGeneratedDataframeCommandOption);
    }
    addCommand(id, opts) {
        const disposable = this._commands.addCommand(id, opts);
        this._commandsDisposeMap.set(id, disposable);
    }
    removeCommand(id) {
        if (!this._commands.hasCommand(id)) {
            return false;
        }
        const disposable = this._commandsDisposeMap.get(id);
        if (!disposable) {
            return false;
        }
        disposable.dispose();
        this._commandsDisposeMap.delete(id);
        return true;
    }
    execute(id, args) {
        return this._commands.execute(id, args);
    }
    get registry() {
        return this._commands;
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _cells__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./cells */ "./lib/cells/trrackableCellFactory.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./notebook */ "./lib/notebook/index.js");
/* harmony import */ var _utils_globals__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./utils/globals */ "./lib/utils/globals.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);








/**
 * Initialization data for the persist_ext extension.
 */
const plugin = {
    id: 'persist_ext:plugin',
    description: 'PersIst is a JupyterLab extension to enable persistent interactive visualizations in JupyterLab notebooks.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    activate: (_app, nbTracker, settingRegistry) => {
        // Setup window.Persist
        console.log('Setting up persist');
        (0,_utils_globals__WEBPACK_IMPORTED_MODULE_5__.setupPersist)();
        // Listen to notebook changes
        nbTracker.currentChanged.connect((_, nbPanel) => {
            const wrapper = new _notebook__WEBPACK_IMPORTED_MODULE_6__.NotebookWrapper(nbPanel);
            window.Persist.Notebook = wrapper;
            wrapper.setupFinish.then(() => {
                console.log(wrapper.nbUid, 'is ready!');
            });
        });
        console.log('JupyterLab extension persist_ext is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('persist_ext settings loaded:', settings);
            })
                .catch(reason => {
                console.error('Failed to load settings for persist_ext.', reason);
            });
        }
    }
};
const TRRACKABLE_CELL_PLUGIN = 'persist_ext:trrackable-cell-plugin';
const trrackableCellPlugin = {
    id: TRRACKABLE_CELL_PLUGIN,
    description: 'Trrackable cell plugin companion',
    autoStart: true,
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.ICommandPalette],
    activate: (app, editor, palette) => {
        console.log('JupyterLab extension trrackable-persist-cell is activated!');
        const { commands } = app;
        const clearPersistMetaCommand = 'persist:meta:clear';
        const clearPersistResetAllTrrack = 'persist:meta:reset-all-trrack';
        commands.addCommand(clearPersistResetAllTrrack, {
            label: 'Reset Trrack instances for all cells',
            execute: () => {
                window.Persist.CellMap.forEach(cell => {
                    if (cell === null || cell === void 0 ? void 0 : cell._trrackManager) {
                        cell === null || cell === void 0 ? void 0 : cell.trrackManager.reset();
                    }
                });
                window.Persist.Notebook.save();
            }
        });
        commands.addCommand(clearPersistMetaCommand, {
            label: 'Clear all persist metadata from cells and the notebook',
            execute: () => {
                const keys = window.Persist.Notebook.getPersistKeyRecord();
                keys.push('__CATEGORIES__', '__USER_ADDED_CATEGORIES__');
                keys.forEach(key => {
                    window.Persist.Notebook.metadata.write(key, _notebook__WEBPACK_IMPORTED_MODULE_6__.DELETE_NB_METADATA);
                });
                commands.execute(clearPersistResetAllTrrack);
                window.Persist.CellMap.forEach(cell => {
                    keys.forEach(k => { var _a; return (_a = cell === null || cell === void 0 ? void 0 : cell.model) === null || _a === void 0 ? void 0 : _a.deleteMetadata(k); });
                });
                window.Persist.Notebook.save();
                console.log('Cleared persist keys and saved!');
            }
        });
        palette.addItem({
            category: 'Persist',
            command: clearPersistMetaCommand
        });
        const factory = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell.ContentFactory({
            editorFactory: editor.factoryService.newInlineEditor
        });
        return new _cells__WEBPACK_IMPORTED_MODULE_7__.TrrackableCellFactory(factory);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, trrackableCellPlugin]);


/***/ }),

/***/ "./lib/interactions/annotate.js":
/*!**************************************!*\
  !*** ./lib/interactions/annotate.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   annotateCommandOption: () => (/* binding */ annotateCommandOption),
/* harmony export */   createAnnotateActionAndLabelLike: () => (/* binding */ createAnnotateActionAndLabelLike)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/interactions/base.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");



function createAnnotateActionAndLabelLike(text) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'annotate',
            text,
            createdOn: Date.now()
        },
        label: () => {
            return 'Add annotation to selection: ' + text;
        }
    };
}
const annotateCommandOption = {
    isEnabled(args) {
        return (0,_base__WEBPACK_IMPORTED_MODULE_1__.hasSelections)(args);
    },
    execute(args) {
        const { cell, text } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_2__.castArgs)(args);
        const { action, label } = createAnnotateActionAndLabelLike(text);
        return cell.trrackManager.apply(action, label);
    }
};


/***/ }),

/***/ "./lib/interactions/base.js":
/*!**********************************!*\
  !*** ./lib/interactions/base.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   hasSelections: () => (/* binding */ hasSelections)
/* harmony export */ });
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");
/* harmony import */ var _widgets_trrack_utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../widgets/trrack/utils */ "./lib/widgets/trrack/utils.js");


function hasSelections(args) {
    const { cell } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_0__.castArgs)(args);
    const trrack = cell.trrackManager.trrack;
    const interaction = trrack.getState();
    return (0,_widgets_trrack_utils__WEBPACK_IMPORTED_MODULE_1__.isAnySelectionInteraction)(interaction);
}


/***/ }),

/***/ "./lib/interactions/categorize.js":
/*!****************************************!*\
  !*** ./lib/interactions/categorize.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   categorizeCommandOption: () => (/* binding */ categorizeCommandOption),
/* harmony export */   createCategorizeActionAndLabelLike: () => (/* binding */ createCategorizeActionAndLabelLike)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createCategorizeActionAndLabelLike(action) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'category',
            action
        },
        label: () => {
            let label = '';
            switch (action.op) {
                case 'add':
                    label += 'Add ';
                    break;
                case 'remove':
                    label += 'Remove ';
                    break;
                case 'assign':
                    label += 'Assign ';
                    break;
                case 'reorder':
                    label += `Reorder options for '${action.category}'`;
                    break;
            }
            switch (action.scope) {
                case 'category':
                    label += `new category '${action.category}'`;
                    break;
                case 'option':
                    if (action.op === 'assign') {
                        label += `'${action.category} (${action.option})' to selected items.`;
                    }
                    else {
                        label += `'${action.option}' ${action.op === 'add' ? 'to' : 'from'} ${action.category}`;
                    }
                    break;
            }
            return label;
        }
    };
}
// Command Option
const categorizeCommandOption = {
    execute(args) {
        const { cell, action, overrideLabel } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action: act, label } = createCategorizeActionAndLabelLike(action);
        return cell.trrackManager.apply(act, overrideLabel ? overrideLabel : label);
    },
    label: 'Assign Category'
};


/***/ }),

/***/ "./lib/interactions/changeColumnType.js":
/*!**********************************************!*\
  !*** ./lib/interactions/changeColumnType.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   changeColumnTypeCommandOption: () => (/* binding */ changeColumnTypeCommandOption),
/* harmony export */   createChangeColumnTypeActionAndLabelLike: () => (/* binding */ createChangeColumnTypeActionAndLabelLike)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createChangeColumnTypeActionAndLabelLike(columnDataTypes) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'column_type_change',
            columnDataTypes
        },
        label: () => {
            const changes = Object.entries(columnDataTypes);
            if (changes.length === 1) {
                return `Changed column '${changes[0][0]}' type to '${changes[0][1].type}'`;
            }
            if (changes.length > 1) {
                return `Changed types for ${changes.length} columns`;
            }
            return 'Change columns';
        }
    };
}
// Command Option
const changeColumnTypeCommandOption = {
    execute(args) {
        const { cell, columnDataTypes } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createChangeColumnTypeActionAndLabelLike(columnDataTypes);
        return cell.trrackManager.apply(action, label);
    },
    label: 'Reorder Columns'
};


/***/ }),

/***/ "./lib/interactions/dropColumn.js":
/*!****************************************!*\
  !*** ./lib/interactions/dropColumn.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createDropColumnsActionAndLabelLike: () => (/* binding */ createDropColumnsActionAndLabelLike),
/* harmony export */   dropColumnsCommandOption: () => (/* binding */ dropColumnsCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createDropColumnsActionAndLabelLike(columns) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'drop_columns',
            columns
        },
        label: () => {
            return columns.length > 1
                ? `Drop ${columns.length} columns`
                : `Drop column ${columns[0]}`;
        }
    };
}
// Command Option
const dropColumnsCommandOption = {
    execute(args) {
        const { cell, columns } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createDropColumnsActionAndLabelLike(columns);
        return cell.trrackManager.apply(action, label);
    },
    label: 'Drop Columns'
};


/***/ }),

/***/ "./lib/interactions/editCell.js":
/*!**************************************!*\
  !*** ./lib/interactions/editCell.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createEditCellActionAndLabelLike: () => (/* binding */ createEditCellActionAndLabelLike),
/* harmony export */   editCellCommandOption: () => (/* binding */ editCellCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createEditCellActionAndLabelLike(columnName, idx, value) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'edit_cell',
            columnName,
            idx,
            value
        },
        label: () => {
            return `Updated column '${columnName}', idx ${idx} to '${value}'`;
        }
    };
}
// Command Option
const editCellCommandOption = {
    execute(args) {
        const { cell, columnName, idx, value } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createEditCellActionAndLabelLike(columnName, idx, value);
        return cell.trrackManager.apply(action, label);
    },
    label: 'Reorder Columns'
};


/***/ }),

/***/ "./lib/interactions/filter.js":
/*!************************************!*\
  !*** ./lib/interactions/filter.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createFilterActionAndLabelLike: () => (/* binding */ createFilterActionAndLabelLike),
/* harmony export */   filterCommandOption: () => (/* binding */ filterCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base */ "./lib/interactions/base.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");



// Action Creator
function createFilterActionAndLabelLike(direction) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'filter',
            direction
        },
        label: () => {
            return direction === 'out'
                ? 'Removed selected items'
                : 'Kept selected items';
        }
    };
}
// Command Option
const filterCommandOption = {
    isEnabled(args) {
        return (0,_base__WEBPACK_IMPORTED_MODULE_1__.hasSelections)(args);
    },
    execute(args) {
        const { cell, direction } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_2__.castArgs)(args);
        const { action, label } = createFilterActionAndLabelLike(direction);
        return cell.trrackManager.apply(action, label);
    },
    label: args => {
        const { direction } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_2__.castArgs)(args);
        return direction === 'out' ? 'Remove selection' : 'Keep only selection';
    }
};


/***/ }),

/***/ "./lib/interactions/intentSelection.js":
/*!*********************************************!*\
  !*** ./lib/interactions/intentSelection.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createIntentSelectionActionAndLabelLike: () => (/* binding */ createIntentSelectionActionAndLabelLike),
/* harmony export */   intentSelectionCommandOption: () => (/* binding */ intentSelectionCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");
/* harmony import */ var _utils_jsonHelpers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/jsonHelpers */ "./lib/utils/jsonHelpers.js");



// Action Creator
function createIntentSelectionActionAndLabelLike(intent, selected) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'intent',
            intent,
            ...selected
        },
        label: () => {
            return `Selected ${intent.intent}`;
        }
    };
}
// Command Option
const intentSelectionCommandOption = {
    execute(args) {
        const { intent, cell, name, value, store, brush_type } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createIntentSelectionActionAndLabelLike(intent, {
            value,
            name,
            store: (0,_utils_jsonHelpers__WEBPACK_IMPORTED_MODULE_2__.parseStringify)(store),
            brush_type
        });
        return cell.trrackManager.apply(action, label);
    }
};


/***/ }),

/***/ "./lib/interactions/renameColumn.js":
/*!******************************************!*\
  !*** ./lib/interactions/renameColumn.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createRenameColumnActionAndLabelLike: () => (/* binding */ createRenameColumnActionAndLabelLike),
/* harmony export */   renameColumnCommandOption: () => (/* binding */ renameColumnCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createRenameColumnActionAndLabelLike(renameColumnMap) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'rename_column',
            renameColumnMap
        },
        label: () => {
            const entries = Object.entries(renameColumnMap);
            if (entries.length === 0) {
                return 'Rename Action';
            }
            if (entries.length === 1) {
                return `Rename column ${entries[0][0]} to ${entries[0][1]}`;
            }
            return `Rename ${entries.length} columns`;
        }
    };
}
// Command Option
const renameColumnCommandOption = {
    execute(args) {
        const { cell, renameColumnMap } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createRenameColumnActionAndLabelLike(renameColumnMap);
        return cell.trrackManager.apply(action, label);
    },
    label: 'Rename Column'
};


/***/ }),

/***/ "./lib/interactions/reorderColumns.js":
/*!********************************************!*\
  !*** ./lib/interactions/reorderColumns.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createReorderColumnsActionAndLabelLike: () => (/* binding */ createReorderColumnsActionAndLabelLike),
/* harmony export */   reorderColumnsCommandOption: () => (/* binding */ reorderColumnsCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createReorderColumnsActionAndLabelLike(columns) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'reorder_column',
            columns
        },
        label: () => {
            return 'Reorder columns';
        }
    };
}
// Command Option
const reorderColumnsCommandOption = {
    execute(args) {
        const { cell, columns, overrideLabel } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        if (columns.length === 0) {
            return;
        }
        const { action, label } = createReorderColumnsActionAndLabelLike(columns);
        return cell.trrackManager.apply(action, overrideLabel ? overrideLabel : label);
    },
    label: 'Reorder Columns'
};


/***/ }),

/***/ "./lib/interactions/selection.js":
/*!***************************************!*\
  !*** ./lib/interactions/selection.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createSelectionActionAndLabelLike: () => (/* binding */ createSelectionActionAndLabelLike),
/* harmony export */   selectionCommandOption: () => (/* binding */ selectionCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");
/* harmony import */ var _utils_jsonHelpers__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils/jsonHelpers */ "./lib/utils/jsonHelpers.js");
/* harmony import */ var vega_lite__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vega-lite */ "webpack/sharing/consume/default/vega-lite/vega-lite");
/* harmony import */ var vega_lite__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(vega_lite__WEBPACK_IMPORTED_MODULE_0__);




// Action Creator
function createSelectionActionAndLabelLike(selected) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_1__.UUID)(),
            type: 'select',
            ...selected
        },
        label: () => {
            const { brush_type, name, value, store } = selected;
            if (brush_type === 'non-vega') {
                const v = value;
                if (v.length === 1) {
                    return `Selected ${v.length} point`;
                }
                if (v.length === 0) {
                    return 'Clear selections';
                }
                return `Selected ${v.length} points`;
            }
            if (store.length === 0) {
                return 'Clear selections';
            }
            if (brush_type === 'non-vega-null') {
                return `Selected missing or invalid for '${name}'`;
            }
            if (store.length === 0) {
                return 'Clear selections';
            }
            if (brush_type === 'interval') {
                const val = value;
                const sel_strings = [];
                Object.entries(val).forEach(([k, v]) => {
                    const str = `${k} (${v[0] instanceof Date
                        ? v[0].toUTCString()
                        : (0,vega_lite__WEBPACK_IMPORTED_MODULE_0__.isNumeric)(v[0])
                            ? Math.round(v[0])
                            : v[0]} to ${v[v.length - 1] instanceof Date
                        ? v[v.length - 1].toUTCString()
                        : (0,vega_lite__WEBPACK_IMPORTED_MODULE_0__.isNumeric)(v[v.length - 1])
                            ? Math.round(v[v.length - 1])
                            : v[v.length - 1]})`;
                    sel_strings.push(str);
                });
                return 'Selected ' + sel_strings.join(', ');
            }
            else {
                const val = value;
                if (val['vlPoint'] && val['vlPoint']['or']) {
                    const arr = val.vlPoint.or;
                    if (arr.length > 0) {
                        return `Selected ${arr.length} ${arr.length === 1 ? 'point' : 'points'} across ${Object.keys(arr[0]).join(', ')}`;
                    }
                }
                else if (name === 'index_selection') {
                    const arr = value;
                    return arr.length === 1
                        ? `Selected ${arr.length} point`
                        : `Selected ${arr.length} points`;
                }
            }
            return 'Selected Points!';
        }
    };
}
// Command Option
const selectionCommandOption = {
    execute(args) {
        const { cell, name, value, store, brush_type } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_2__.castArgs)(args);
        const { action, label } = createSelectionActionAndLabelLike({
            value,
            name,
            store: (0,_utils_jsonHelpers__WEBPACK_IMPORTED_MODULE_3__.parseStringify)(store),
            brush_type
        });
        return cell.trrackManager.apply(action, label);
    }
};


/***/ }),

/***/ "./lib/interactions/sortByColumn.js":
/*!******************************************!*\
  !*** ./lib/interactions/sortByColumn.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createSortByColumnActionAndLabelLike: () => (/* binding */ createSortByColumnActionAndLabelLike),
/* harmony export */   sortbyColumnCommandOption: () => (/* binding */ sortbyColumnCommandOption)
/* harmony export */ });
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/castArgs */ "./lib/utils/castArgs.js");


// Action Creator
function createSortByColumnActionAndLabelLike(sortStatus) {
    return {
        action: {
            id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_0__.UUID)(),
            type: 'sortby_column',
            sortStatus
        },
        label: () => {
            if (sortStatus.length === 0) {
                return 'Reset sorting';
            }
            const sortStrings = sortStatus.map(s => `Sort (${s.desc ? 'descending' : 'ascending'}) by '${s.id}'`);
            return sortStrings.length === 1
                ? sortStrings[0]
                : `Sort by ${sortStrings.length} columns. ${sortStrings.join('|\n')}`;
        }
    };
}
// Command Option
const sortbyColumnCommandOption = {
    execute(args) {
        const { cell, sortStatus } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        const { action, label } = createSortByColumnActionAndLabelLike(sortStatus);
        return cell.trrackManager.apply(action, label);
    },
    label: 'Sort Column'
};


/***/ }),

/***/ "./lib/notebook/index.js":
/*!*******************************!*\
  !*** ./lib/notebook/index.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DELETE_NB_METADATA: () => (/* binding */ DELETE_NB_METADATA),
/* harmony export */   NotebookWrapper: () => (/* binding */ NotebookWrapper)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/uuid */ "./lib/utils/uuid.js");


const NOTEBOOK_UUID = '__persist_nb_uuid__';
const PERSIST_KEYS_RECORD = '__persist_keys_record';
const DELETE_NB_METADATA = Symbol('__delete_nb_metadata');
class NotebookWrapper {
    constructor(_nbPanel = null) {
        var _a;
        this._nbPanel = _nbPanel;
        this._setupFinishDelegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._nb = _nbPanel === null || _nbPanel === void 0 ? void 0 : _nbPanel.content;
        (_a = this._nbPanel) === null || _a === void 0 ? void 0 : _a.context.ready.then(() => {
            return onContextReady(this);
        }).then(() => {
            this.udpatePersistKeyRecord(NOTEBOOK_UUID);
            this._setupFinishDelegate.resolve();
        });
    }
    get nb() {
        return this._nb;
    }
    get nbPanel() {
        return this._nbPanel;
    }
    get model() {
        var _a;
        return (_a = this._nbPanel) === null || _a === void 0 ? void 0 : _a.model;
    }
    get setupFinish() {
        return this._setupFinishDelegate.promise;
    }
    get nbUid() {
        var _a;
        return (_a = this.model) === null || _a === void 0 ? void 0 : _a.getMetadata(NOTEBOOK_UUID);
    }
    forEachCell(fn) {
        var _a;
        const cells = (_a = this.model) === null || _a === void 0 ? void 0 : _a.cells;
        if (!cells) {
            return;
        }
        for (let i = 0; i < cells.length; ++i) {
            const cell = cells.get(i);
            fn(cell);
        }
    }
    udpatePersistKeyRecord(key, overwrite = false) {
        const persistKeys = this.metadata.get(PERSIST_KEYS_RECORD) || [];
        if (overwrite) {
            persistKeys.splice(0, persistKeys.length);
        }
        const keys = (typeof key === 'string' ? [key] : key).filter(k => !persistKeys.includes(k));
        persistKeys.push(...keys);
        if (persistKeys.length > 0) {
            this.metadata.write(PERSIST_KEYS_RECORD, [...new Set(persistKeys)]);
        }
    }
    getPersistKeyRecord() {
        return this.metadata.get(PERSIST_KEYS_RECORD) || [];
    }
    get metadata() {
        const model = this.model;
        function get(key) {
            return model === null || model === void 0 ? void 0 : model.getMetadata(key);
        }
        function write(key, value) {
            if (value === DELETE_NB_METADATA) {
                model === null || model === void 0 ? void 0 : model.deleteMetadata(key);
            }
            else {
                model === null || model === void 0 ? void 0 : model.setMetadata(key, value);
            }
        }
        return {
            get,
            write
        };
    }
    save(saveAs = false) {
        var _a, _b;
        if (saveAs) {
            return (_a = this._nbPanel) === null || _a === void 0 ? void 0 : _a.context.saveAs();
        }
        else {
            return (_b = this._nbPanel) === null || _b === void 0 ? void 0 : _b.context.save();
        }
    }
}
async function onContextReady(nb) {
    await saveUUID(nb);
    return Promise.resolve();
}
async function saveUUID(nb) {
    if (nb.model) {
        const hasUid = !!nb.nbUid;
        if (!hasUid) {
            nb.model.setMetadata(NOTEBOOK_UUID, (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_1__.UUID)());
            await nb.save();
        }
    }
    return Promise.resolve();
}


/***/ }),

/***/ "./lib/utils/castArgs.js":
/*!*******************************!*\
  !*** ./lib/utils/castArgs.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   castArgs: () => (/* binding */ castArgs)
/* harmony export */ });
function castArgs(args) {
    return args;
}


/***/ }),

/***/ "./lib/utils/cellStoreEngine.js":
/*!**************************************!*\
  !*** ./lib/utils/cellStoreEngine.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   decompressString: () => (/* binding */ decompressString),
/* harmony export */   getCellStoreEngine: () => (/* binding */ getCellStoreEngine)
/* harmony export */ });
/* harmony import */ var lz_string__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lz-string */ "webpack/sharing/consume/default/lz-string/lz-string");
/* harmony import */ var lz_string__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lz_string__WEBPACK_IMPORTED_MODULE_0__);

function decompressString(s) {
    return (0,lz_string__WEBPACK_IMPORTED_MODULE_0__.decompressFromUTF16)(s);
}
function getCellStoreEngine(cell) {
    return {
        getItem(key) {
            window.Persist.Notebook.udpatePersistKeyRecord(key);
            const val = cell.model.getMetadata(key);
            const processedString = val ? decompressString(val) : val; // decompress if needed
            return processedString;
        },
        setItem(key, value) {
            cell.model.setMetadata(key, value ? (0,lz_string__WEBPACK_IMPORTED_MODULE_0__.compressToUTF16)(value) : value);
        },
        removeItem(key) {
            return cell.model.deleteMetadata(key);
        }
    };
}


/***/ }),

/***/ "./lib/utils/globals.js":
/*!******************************!*\
  !*** ./lib/utils/globals.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   setupPersist: () => (/* binding */ setupPersist)
/* harmony export */ });
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../commands */ "./lib/commands/index.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../notebook */ "./lib/notebook/index.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);



/**
 * The function `setupPersist` initializes the `Persist` object with a `CellMap`, `Commands`, and
 * `Notebook` property.
 */
function setupPersist() {
    window.Persist = {
        CellMap: new Map(),
        Commands: new _commands__WEBPACK_IMPORTED_MODULE_1__.PersistCommandRegistry(),
        Notebook: new _notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookWrapper(),
        Views: new WeakMap(),
        Notification: {
            notify(...args) {
                return _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.emit(...args);
            }
        }
    };
}


/***/ }),

/***/ "./lib/utils/jsonHelpers.js":
/*!**********************************!*\
  !*** ./lib/utils/jsonHelpers.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   parse: () => (/* binding */ parse),
/* harmony export */   parseStringify: () => (/* binding */ parseStringify),
/* harmony export */   stringify: () => (/* binding */ stringify)
/* harmony export */ });
function stringify(val) {
    return JSON.stringify(val);
}
function parse(str) {
    return JSON.parse(str);
}
function parseStringify(obj) {
    if (!obj) {
        return obj;
    }
    return parse(stringify(obj));
}


/***/ }),

/***/ "./lib/utils/stripImmutableClone.js":
/*!******************************************!*\
  !*** ./lib/utils/stripImmutableClone.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   stripImmutableClone: () => (/* binding */ stripImmutableClone),
/* harmony export */   stripImmutableCloneJSON: () => (/* binding */ stripImmutableCloneJSON)
/* harmony export */ });
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_0__);

function stripImmutableClone(ob) {
    return (0,lodash__WEBPACK_IMPORTED_MODULE_0__.cloneDeep)(ob);
}
function stripImmutableCloneJSON(ob) {
    return JSON.parse(JSON.stringify(ob));
}


/***/ }),

/***/ "./lib/utils/uuid.js":
/*!***************************!*\
  !*** ./lib/utils/uuid.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   UUID: () => (/* binding */ UUID)
/* harmony export */ });
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! uuid */ "webpack/sharing/consume/default/uuid/uuid");
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(uuid__WEBPACK_IMPORTED_MODULE_0__);

function UUID() {
    return (0,uuid__WEBPACK_IMPORTED_MODULE_0__.v4)();
}


/***/ }),

/***/ "./lib/widgets/trrack/labelGen.js":
/*!****************************************!*\
  !*** ./lib/widgets/trrack/labelGen.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getLabelFromLabelLike: () => (/* binding */ getLabelFromLabelLike)
/* harmony export */ });
function getLabelFromLabelLike(label) {
    return typeof label === 'function' ? label() : label;
}


/***/ }),

/***/ "./lib/widgets/trrack/manager.js":
/*!***************************************!*\
  !*** ./lib/widgets/trrack/manager.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TrrackManager: () => (/* binding */ TrrackManager)
/* harmony export */ });
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @trrack/core */ "webpack/sharing/consume/default/@trrack/core/@trrack/core");
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_trrack_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils_uuid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../utils/uuid */ "./lib/utils/uuid.js");
/* harmony import */ var _labelGen__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./labelGen */ "./lib/widgets/trrack/labelGen.js");
/* harmony import */ var _hookstate_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @hookstate/core */ "webpack/sharing/consume/default/@hookstate/core/@hookstate/core?4643");
/* harmony import */ var _hookstate_core__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_hookstate_core__WEBPACK_IMPORTED_MODULE_2__);





const defaultTrrackState = {
    id: (0,_utils_uuid__WEBPACK_IMPORTED_MODULE_3__.UUID)(),
    type: 'create'
};
class TrrackManager {
    static getInstance(cell) {
        return new TrrackManager(cell);
    }
    constructor(_cell) {
        this._cell = _cell;
        this._notifyTrrackInstanceChange = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._registry = _trrack_core__WEBPACK_IMPORTED_MODULE_0__.Registry.create();
        this._notifyCurrentChange = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._unsubscribeCurrentChangeListener = null;
        this.undoRedoStatus = (0,_hookstate_core__WEBPACK_IMPORTED_MODULE_2__.hookstate)({
            canUndo: false,
            canRedo: false
        });
        TrrackManager._instanceMaps.set(_cell, this);
        this._addInteractionAction = this._registerAddInteractionAction();
        this.loadTrrack(this._cell.trrackGraph);
    }
    get trrackInstanceChange() {
        return this._notifyTrrackInstanceChange;
    }
    get currentChange() {
        return this._notifyCurrentChange;
    }
    get trrack() {
        return this._trrack;
    }
    reset() {
        this.loadTrrack();
        this._cell.generatedDataframesState.set({});
    }
    saveToJupyter() {
        this._cell.trrackGraphState.set(this._graph);
    }
    loadTrrack(graphToLoad = null) {
        const onCurrentChange = () => {
            this._cell.trrackGraphState.set(this._graph);
            this.undoRedoStatus
                .nested('canUndo')
                .set(this.trrack.current.id !== this.trrack.root.id);
            this.undoRedoStatus
                .nested('canRedo')
                .set(this.trrack.current.children.length > 0);
            window.Persist.Commands.registry.notifyCommandChanged();
            this._notifyCurrentChange.emit(this._trrack.current.id);
        };
        if (this._unsubscribeCurrentChangeListener) {
            this._unsubscribeCurrentChangeListener();
        }
        this._trrack = (0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.initializeTrrack)({
            registry: this._registry,
            initialState: defaultTrrackState
        });
        if (graphToLoad && graphToLoad.root !== this._trrack.root.id) {
            this._trrack.importObject(graphToLoad);
        }
        this._unsubscribeCurrentChangeListener =
            this._trrack.currentChange(onCurrentChange);
        onCurrentChange();
        this._notifyTrrackInstanceChange.emit(this._trrack);
    }
    apply(action, label) {
        return this._trrack.apply((0,_labelGen__WEBPACK_IMPORTED_MODULE_4__.getLabelFromLabelLike)(label), this._addInteractionAction(action));
    }
    get _graph() {
        return this._trrack.exportObject();
    }
    _registerAddInteractionAction() {
        return (interaction) => {
            if (!this._registry.has(interaction.type)) {
                this._registry.register(interaction.type, (_, interaction) => {
                    return interaction;
                });
            }
            return {
                type: interaction.type,
                payload: interaction
            };
        };
    }
}
TrrackManager._instanceMaps = new WeakMap();



/***/ }),

/***/ "./lib/widgets/trrack/utils.js":
/*!*************************************!*\
  !*** ./lib/widgets/trrack/utils.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getInteractionsFromRoot: () => (/* binding */ getInteractionsFromRoot),
/* harmony export */   isAnySelectionInteraction: () => (/* binding */ isAnySelectionInteraction)
/* harmony export */ });
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @trrack/core */ "webpack/sharing/consume/default/@trrack/core/@trrack/core");
/* harmony import */ var _trrack_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_trrack_core__WEBPACK_IMPORTED_MODULE_0__);

function getInteractionsFromRoot(trrack, till = trrack.current.id) {
    const ids = [];
    const nodes = trrack.graph.backend.nodes;
    let node = nodes[till];
    while (!(0,_trrack_core__WEBPACK_IMPORTED_MODULE_0__.isRootNode)(node)) {
        ids.push(node.id);
        node = nodes[node.parent];
    }
    ids.push(trrack.root.id);
    ids.reverse();
    return ids.map(i => nodes[i]).map(node => trrack.getState(node));
}
function isAnySelectionInteraction(interaction) {
    return interaction.type === 'select';
}


/***/ }),

/***/ "./lib/widgets/utils/dataframe.js":
/*!****************************************!*\
  !*** ./lib/widgets/utils/dataframe.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   copyGeneratedDataframeCommandOption: () => (/* binding */ copyGeneratedDataframeCommandOption),
/* harmony export */   createDataframeCommandOption: () => (/* binding */ createDataframeCommandOption),
/* harmony export */   deleteGeneratedDataframeCommandOption: () => (/* binding */ deleteGeneratedDataframeCommandOption),
/* harmony export */   getRecord: () => (/* binding */ getRecord),
/* harmony export */   insertCellWithGeneratedDataframeCommandOption: () => (/* binding */ insertCellWithGeneratedDataframeCommandOption),
/* harmony export */   postCreationAction: () => (/* binding */ postCreationAction)
/* harmony export */ });
/* harmony import */ var _utils_castArgs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../utils/castArgs */ "./lib/utils/castArgs.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../commands */ "./lib/commands/index.js");
/* harmony import */ var _trrack_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../trrack/utils */ "./lib/widgets/trrack/utils.js");




// Command Option
const createDataframeCommandOption = {
    execute(args) {
        const { record, model, post } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        model.set('gdr_signal', {
            record,
            post
        });
        model.save_changes();
    }
};
const deleteGeneratedDataframeCommandOption = {
    execute(args) {
        const { cell } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        cell;
    },
    label: 'Delete generated dataframe'
};
const copyGeneratedDataframeCommandOption = {
    execute(args) {
        const { record } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        copyDFNameToClipboard(record.dfName)
            .then(() => {
            notifyCopySuccess(record.dfName);
        })
            .catch(err => {
            console.error(err);
            notifyCopyFailure(record.dfName, err);
        });
    }
};
const insertCellWithGeneratedDataframeCommandOption = {
    execute(args) {
        const { record } = (0,_utils_castArgs__WEBPACK_IMPORTED_MODULE_1__.castArgs)(args);
        addCellWithDataframeVariable(`${record.dfName}.head()`);
    }
};
function postCreationAction(record, action) {
    if (action === 'copy') {
        window.Persist.Commands.execute(_commands__WEBPACK_IMPORTED_MODULE_2__.PersistCommands.copyDataframe, { record });
    }
    else if (action === 'insert') {
        window.Persist.Commands.execute(_commands__WEBPACK_IMPORTED_MODULE_2__.PersistCommands.insertCellWithDataframe, {
            record
        });
    }
}
async function copyDFNameToClipboard(name) {
    return await navigator.clipboard.writeText(name);
}
function notifyCopyFailure(name, error) {
    window.Persist.Notification.notify(`Failed to copy ${name} to clipboard. ${error}`, 'error', {
        autoClose: 500
    });
}
function notifyCopySuccess(dfName) {
    window.Persist.Notification.notify(`Copied code for df: ${dfName}`, 'success', {
        autoClose: 500
    });
}
function addCellWithDataframeVariable(dfName) {
    var _a, _b;
    const currentNotebook = (_a = window.Persist.Notebook.nbPanel) === null || _a === void 0 ? void 0 : _a.content;
    if (!currentNotebook) {
        return;
    }
    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.insertBelow(currentNotebook);
    const newCell = currentNotebook.activeCell;
    if (!newCell) {
        return;
    }
    const text = newCell.model.sharedModel.getSource();
    if (text.length > 0) {
        throw new Error('New codecell should have no content!');
    }
    newCell.model.sharedModel.setSource(dfName);
    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(currentNotebook, (_b = window.Persist.Notebook.nbPanel) === null || _b === void 0 ? void 0 : _b.sessionContext);
    newCell.node.scrollIntoView(true);
}
function getRecord(dfName, trrack, isDynamic) {
    return {
        dfName,
        root_id: trrack.root.id,
        current_node_id: trrack.current.id,
        interactions: (0,_trrack_utils__WEBPACK_IMPORTED_MODULE_3__.getInteractionsFromRoot)(trrack),
        isDynamic
    };
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8b8fd816e26e671f9935.js.map