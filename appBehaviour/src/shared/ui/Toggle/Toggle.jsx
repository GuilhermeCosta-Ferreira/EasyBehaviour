import { useEffect, useState } from "react";

import Dropdown from 'react-bootstrap/Dropdown';
import SingleToggle from '../SingleToggle/SingleToggle';

import dropdown_style from "../Dropdown/Dropdown.module.css"
import style from "./Toggle.module.css"

function Toggle({
  title = "Select One or More",
  options = [],
  className = "",
  filterCall
}) {
  const [opt, setOpt] = useState([]);


  const toggleOption = (clickedOption) => {
      setOpt((prev) =>
        prev.includes(clickedOption)
          ? prev.filter((t) => t !== clickedOption)
          : [clickedOption, ...prev]
      );
    };

    // ✅ side-effect happens AFTER render
    useEffect(() => {
      filterCall?.(title, opt);
    }, [title, opt, filterCall]);


  return (
    <Dropdown className={`${className} ${dropdown_style.dropdown} ${style.main}`}>
      <Dropdown.Toggle className={`${style.container} ${dropdown_style.toggle}`}>{title}</Dropdown.Toggle>

      <Dropdown.Menu className={dropdown_style.menu}>

        {options.length === 0 ? (
          <Dropdown.Item
            className={dropdown_style.item}
            as="span"
            disabled> No items </Dropdown.Item>
        ) : (
          options.map((item, index) => (
            <div
              onClick={() => toggleOption(item)}
              className={style.item_container}
              key={`${item}-${index}`}>
              <SingleToggle>{item}</SingleToggle>
            </div>
          ))
        )}
      </Dropdown.Menu>
    </Dropdown>
  )
}

export default Toggle
