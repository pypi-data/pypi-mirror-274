import { CommandRegistry } from '@lumino/commands';
import { UUID } from '../utils/uuid';
import {
  ActionAndLabelLike,
  BaseCommandArg,
  BaseInteraction,
  hasSelections
} from './base';
import { castArgs } from '../utils/castArgs';

export type FilterDirection = 'in' | 'out';

// Action
export type FilterAction = BaseInteraction & {
  type: 'filter';
  direction: FilterDirection;
};

// Action Creator
export function createFilterActionAndLabelLike(
  direction: FilterDirection
): ActionAndLabelLike<FilterAction> {
  return {
    action: {
      id: UUID(),
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

// Command
export type FilterCommandArgs = BaseCommandArg & {
  direction: FilterDirection;
};

// Command Option
export const filterCommandOption: CommandRegistry.ICommandOptions = {
  isEnabled(args) {
    return hasSelections(args);
  },
  execute(args) {
    const { cell, direction } = castArgs<FilterCommandArgs>(args);

    const { action, label } = createFilterActionAndLabelLike(direction);

    return cell.trrackManager.apply(action, label);
  },
  label: args => {
    const { direction } = castArgs<FilterCommandArgs>(args);

    return direction === 'out' ? 'Remove selection' : 'Keep only selection';
  }
};
