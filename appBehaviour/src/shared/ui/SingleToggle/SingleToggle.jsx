import { useState } from "react";

import style from './SingleToggle.module.css'

function SingleToggle({ children }) {
  const [toggle, setToggle] = useState(false);

  function updateToggle(current) {
      return current ? false : true;
    }

  return (
    <div
      className={style.group}
      onClick={() => setToggle(updateToggle(toggle))}
    >
      <i className={`bi ${toggle ? "bi-check-square-fill" : "bi-square"} ${style.item}`} />
      <p className={`${style.toggle_text} ${style.item}`}>{children}</p>
    </div>
  );
}

export default SingleToggle
