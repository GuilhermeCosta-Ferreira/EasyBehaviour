function TableViewer({ columns, rows, className='' }) {
  return (
    <div style={{ marginTop: 12 }} className={`${className}`}>
      {rows.length === 0 ? (
        <p>(No rows)</p>
      ) : (
        <table>
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={c}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                {columns.map((c) => (
                  <td key={c}>{String(r[c] ?? "")}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default TableViewer
