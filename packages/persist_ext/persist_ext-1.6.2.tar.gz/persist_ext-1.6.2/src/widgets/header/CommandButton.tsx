import { CommandRegistry } from '@lumino/commands';
import { ReadonlyPartialJSONObject } from '@lumino/coreutils';
import { TrrackableCell } from '../../cells';

import { CommandArgMap } from '../../commands';
import React, { ReactNode } from 'react';
import { UseSignal } from '@jupyterlab/apputils';
import { Tooltip } from '@mantine/core';
import { HeaderActionIcon } from './StyledActionIcon';

export function CommandButton<
  K extends keyof CommandArgMap = keyof CommandArgMap
>({
  cell,
  commandId,
  commandRegistry,
  commandArgs,
  icon,
  isDisabled = undefined
}: {
  cell: TrrackableCell;
  commandRegistry: CommandRegistry;
  commandId: K;
  commandArgs?: Omit<CommandArgMap[K], 'cell'>;
  icon: ReactNode;
  isDisabled?: boolean;
}) {
  if (!commandRegistry || !commandRegistry.hasCommand(commandId)) {
    if (!commandRegistry) {
      console.warn('Command registry not found');
    } else {
      console.warn(`Command ${commandId} not found in registry`);
    }
    return null;
  }

  return (
    <UseSignal signal={commandRegistry.commandChanged}>
      {() => {
        const args = (commandArgs
          ? { ...commandArgs, cell }
          : { cell }) as unknown as ReadonlyPartialJSONObject;

        const isEnabled =
          isDisabled === undefined
            ? commandRegistry.isEnabled(commandId, args)
            : !isDisabled;
        const label = commandRegistry.label(commandId, args) || commandId;

        return (
          <HeaderActionIcon
            variant={isEnabled ? 'subtle' : 'transparent'}
            disabled={!isEnabled}
            onClick={() => commandRegistry.execute(commandId, args)}
          >
            <Tooltip.Floating label={label} offset={20}>
              {icon}
            </Tooltip.Floating>
          </HeaderActionIcon>
        );
      }}
    </UseSignal>
  );
}
