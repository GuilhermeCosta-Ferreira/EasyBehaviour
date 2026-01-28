import style from "./Description.module.css"

function Description({ children }) {
  return <p className={style.description}>{children}</p>
}

export default Description
