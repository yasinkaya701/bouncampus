export default function FoodWasteLoading() {
  return (
    <div className="min-h-screen bg-[#f5f6f5] text-[#111713]">
      <div className="grid min-h-screen lg:grid-cols-[248px_minmax(0,1fr)]">
        <aside className="hidden bg-[#071d18] lg:block" />
        <div>
          <div className="h-[58px] border-b border-[#dfe3df] bg-white" />
          <div className="mx-auto w-full max-w-[1510px] space-y-5 px-4 py-6 sm:px-6 xl:px-7">
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-2">
                <Skeleton className="h-7 w-56" />
                <Skeleton className="h-3 w-72" />
              </div>
              <Skeleton className="h-7 w-24 rounded-md" />
            </div>

            <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
              {Array.from({ length: 4 }).map((_, index) => (
                <Skeleton key={index} className="h-[132px] rounded-xl" />
              ))}
            </div>

            <div className="grid gap-3 xl:grid-cols-[minmax(0,1fr)_360px]">
              <div className="space-y-3">
                <Skeleton className="h-[410px] rounded-xl" />
                <Skeleton className="h-[260px] rounded-xl" />
              </div>
              <div className="space-y-3">
                <Skeleton className="h-[250px] rounded-xl" />
                <Skeleton className="h-[185px] rounded-xl" />
                <Skeleton className="h-[250px] rounded-xl" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Skeleton({ className }: { className: string }) {
  return <div className={`animate-pulse border border-[#e0e4e0] bg-white ${className}`} aria-hidden="true" />;
}
