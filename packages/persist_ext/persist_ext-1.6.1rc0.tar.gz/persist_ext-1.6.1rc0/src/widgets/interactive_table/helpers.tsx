import { useMemo } from 'react';
import React from 'react';
import { MRT_ColumnDef } from 'mantine-react-table';
import { PandasDTypes } from './DTypeContextMenu';
import { Tooltip, Text, createStyles } from '@mantine/core';
import { ColumnHeader } from './ColumnHeader';
import { TrrackableCell } from '../../cells';
import { useModelState } from '@anywidget/react';

export type DataPoint = { K: string } & Record<string, string>;

export type Data = Array<DataPoint>;

export function useColumnDefs(
  cell: TrrackableCell,
  columns: string[],
  idColumn: string,
  data: Data,
  columnsToExclude: string[] = [],
  dTypeMap: Record<string, PandasDTypes> = {}
) {
  const { classes } = useStyles();
  const [categoryColumns] = useModelState<
    Record<string, { name: string; options: string[] }>
  >('df_category_columns');

  return useMemo<MRT_ColumnDef<DataPoint>[]>(() => {
    const cols: MRT_ColumnDef<DataPoint>[] = columns
      .filter(c => !columnsToExclude.includes(c) && c !== idColumn)
      .map(columnKey => ({
        accessorFn: r => {
          return r[columnKey];
        },
        meta: {
          dType: dTypeMap[columnKey],
          values: data.map(d => d[columnKey])
        },
        Header: ({ column }) => (
          <ColumnHeader
            cell={cell}
            column={column}
            allColumns={columns}
            dtype={dTypeMap[column.id]}
          />
        ),
        sortUndefined: 1,
        header: columnKey,
        Cell: ({ renderedCellValue }) => {
          const dtype = dTypeMap[columnKey];

          const val = process_value(renderedCellValue, dtype);

          if (val === null) {
            // console.log(columnKey, val, dtype);
          }

          return (
            <Tooltip label={val} openDelay={200} position="left">
              <Text className={classes.cellHover}>{val}</Text>
            </Tooltip>
          );
        },
        editVariant: dTypeMap[columnKey] === 'category' ? 'select' : 'text',
        mantineEditSelectProps: ({ column }) => {
          let opts: string[] = [];

          if (categoryColumns[column.id]) {
            const cat = categoryColumns[column.id];

            opts = cat.options;
          }

          return {
            size: 'xs',
            data: opts
          };
        },
        mantineEditTextInputProps: ({ row, column }) => {
          return {
            type: getInputType(getDType(columnKey, dTypeMap)),
            dateTime: process_value(
              row.getValue(column.id),
              dTypeMap[column.id],
              true
            )
          };
        }
      }));

    cols.unshift({
      header: idColumn,
      accessorKey: idColumn,
      Header: '#',
      enableClickToCopy: false,
      enableColumnDragging: false,
      enableColumnOrdering: false,
      enableEditing: false,
      enableGrouping: false,
      enableHiding: false,
      enableResizing: false,
      enableSorting: false,
      enablePinning: false,
      enableColumnActions: false,
      maxSize: 70

      // Cell: ({ row, renderedCellValue }) => {
      //   console.log(renderedCellValue);
      //   return row.id;
      // },
    });

    return cols;
  }, [columns, columnsToExclude]);
}

export function applyDTypeToValue(value: string, dtype: PandasDTypes) {
  switch (dtype) {
    case 'Int64':
      try {
        return parseInt(value, 10);
      } catch {
        return value;
      }
    case 'Float64':
      try {
        return parseFloat(value);
      } catch {
        return value;
      }
    case 'boolean':
      return value.toLowerCase() === 'true';
    case 'datetime64[ns]':
      return new Date(value).getTime();
    default:
      return value;
  }
}

export function getDType(
  columnKey: string,
  dTypeMap: Record<string, PandasDTypes>
) {
  return dTypeMap[columnKey] ?? 'string';
}

const useStyles = createStyles(() => ({
  cellHover: {
    '&:hover': {
      transform: 'scale(1.1)',
      transfromOrigin: 'left'
    }
  }
}));

function process_value(renderedCellValue: any, dtype: any, rawDate = false) {
  let val: any = renderedCellValue;

  if (dtype === 'boolean') {
    if (renderedCellValue && renderedCellValue === true) {
      val = 'True';
    } else {
      val = 'False';
    }
  }

  if (dtype.includes('datetime64') && typeof renderedCellValue === 'number') {
    val = new Date(renderedCellValue);

    if (!rawDate) {
      val = val.toLocaleDateString().replace(/\//g, '-');
    } else {
      val = val.toISOString().substring(0, 10);
    }
  }

  if (!val && val !== 0 && ['Int64', 'Float64'].includes(dtype)) {
    val = 'NaN';
  }

  if (!val && dtype === 'datetime64[ns]') {
    val = 'NaT';
  }
  return val;
}

export function getFilterTypeFromDType(type: PandasDTypes) {
  switch (type) {
    case 'Int64':
    case 'Float64':
      return 'range-slider';
    case 'boolean':
      return 'checkbox';
    case 'datetime64[ns]':
      return 'date-range';
    default:
      return 'text';
  }
}

export function getInputType(type: PandasDTypes & any) {
  switch (type) {
    case 'Int64':
    case 'Float64':
      return 'number';
    case 'boolean':
      return 'checkbox';
    case 'datetime64[ns]':
    case 'datetime64[ms, UTC]':
      return 'date';
    default:
      return 'text';
  }
}
