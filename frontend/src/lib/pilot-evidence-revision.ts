/**
 * Revision token for async pilot CSV reads and scoring responses.
 * Later operator actions invalidate earlier results without trusting request timing.
 */
export function createPilotEvidenceRevisionGuard() {
  let revision = 0;
  return {
    invalidate(): number {
      revision += 1;
      return revision;
    },
    isCurrent(candidate: number): boolean {
      return candidate === revision;
    },
  };
}
