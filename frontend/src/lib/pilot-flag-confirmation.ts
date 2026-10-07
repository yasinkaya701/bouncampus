/** Distinguish an operator's explicit "no" from an unanswered pilot flag. */
export type ConfirmablePilotFlags = {
  earlySellout: boolean | null;
  operatorOverride: boolean | null;
};

export function hasConfirmedPilotFlags<T extends ConfirmablePilotFlags>(
  rows: T[],
): rows is (T & { earlySellout: boolean; operatorOverride: boolean })[] {
  return rows.every(row =>
    typeof row.earlySellout === 'boolean' && typeof row.operatorOverride === 'boolean'
  );
}
