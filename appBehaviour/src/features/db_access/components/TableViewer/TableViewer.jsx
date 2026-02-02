import style from './TableViewer.module.css'

function TableViewer({ columns, rows, className = '' }) {
  return (
    <div style={{ marginTop: 12 }} className={`${className} ${style.tableWrap}`}>
      {rows.length === 0 ? (
        <p>(No rows)</p>
      ) : (
        <table className={style.dataTable}>
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
