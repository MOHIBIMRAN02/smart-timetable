export default function ModulePage({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <section className="space-y-4">
      <h1 className="page-title">{title}</h1>
      <div className="card">
        <p className="text-slate-700">{subtitle}</p>
      </div>
    </section>
  );
}
