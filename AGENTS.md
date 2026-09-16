# BOUNCAMPUS Repository Working Policy

## Temporary single-branch rule

Until the repository owner explicitly changes this rule:

- `master` is the only active development branch.
- Make normal engineering changes directly on `master`.
- Do not create feature branches, staging branches, or pull requests for routine work.
- Do not fork work into parallel branches.
- Keep commits small enough to revert safely, but keep all repository truth on `master`.
- CI, validation, and deployment work should also target `master`.
- If a task is risky, preserve safety with commit checkpoints and revertable commits rather than creating another branch.

## Product truth boundary

BOUNCAMPUS must not present model estimates as live university telemetry. Unless a source is explicitly integrated and verified, do not claim access to university BMS, smart meters, turnstiles, Wi-Fi occupancy, cafeteria POS, shuttle GPS, or IoT sensor networks.

## Current release sequence

1. Finish product implementation on `master`.
2. Deploy the `frontend` Next.js application.
3. Validate deployed `/api/v1/health` and core product routes.
4. Run local/CI validation afterward.
5. Refresh the BUIS/ÖBİKAS course snapshot after the 28–30 Sep 2026 add/drop window.
