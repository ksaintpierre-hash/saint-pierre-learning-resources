export function SupportNeedsFields({
  defaults,
}: {
  defaults?: {
    aigIdentified: boolean;
    has504Plan: boolean;
    hasEcIep: boolean;
    extendedTime: boolean;
    accommodationNotes: string;
  };
}) {
  return (
    <fieldset className="flex flex-col gap-3 rounded-lg border border-black/10 p-3">
      <legend className="px-1 text-sm font-medium">Learning support needs (optional)</legend>
      <p className="text-xs text-black/50">
        This helps us tailor course suggestions and pacing. It doesn&apos;t replace your child&apos;s
        official IEP, 504 plan, or AIG paperwork with their school district.
      </p>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="aigIdentified" defaultChecked={defaults?.aigIdentified} />
        AIG identified (Academically/Intellectually Gifted)
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="has504Plan" defaultChecked={defaults?.has504Plan} />
        Has a 504 plan
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="hasEcIep" defaultChecked={defaults?.hasEcIep} />
        Has an IEP / receives EC (Exceptional Children) services
      </label>
      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="extendedTime" defaultChecked={defaults?.extendedTime} />
        Needs extended time on lessons and assignments
      </label>
      <div className="flex flex-col gap-1">
        <label htmlFor="accommodationNotes" className="text-sm font-medium">
          Accommodation notes
        </label>
        <textarea
          id="accommodationNotes"
          name="accommodationNotes"
          className="input"
          rows={2}
          placeholder="e.g. reduced-distraction setting, large print, audio support…"
          defaultValue={defaults?.accommodationNotes}
        />
      </div>
    </fieldset>
  );
}
