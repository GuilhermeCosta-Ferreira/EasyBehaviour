import Dropdown from 'react-bootstrap/Dropdown';
import dropdown_style from "../Dropdown/Dropdown.module.css"
import style from "./Toggle.module.css"
import SingleToggle from '../SingleToggle/SingleToggle';

function Toggle({
  title = "Select One or More",
  options = [],
  className = ""
}) {
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
            <div className={style.item_container} key={`${item}-${index}`}>
              <SingleToggle>{item}</SingleToggle>
            </div>
          ))
        )}
      </Dropdown.Menu>
    </Dropdown>
  )
}

export default Toggle
