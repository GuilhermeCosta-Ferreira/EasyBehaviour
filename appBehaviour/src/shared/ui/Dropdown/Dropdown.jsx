import Dropdown from 'react-bootstrap/Dropdown';
import style from './Dropdown.module.css';

export default function AppDropdown({
  title = 'Dropdown Button',
  items = [],
  onSelect,
  className = "",
}) {
  return (
    <Dropdown className={`${className} ${style.dropdown}`}>
      <Dropdown.Toggle className={style.toggle}>
        {title}
      </Dropdown.Toggle>

      <Dropdown.Menu className={style.menu}>
        {items.length === 0 ? (
          <Dropdown.Item
            className={style.item}
            as="span"
            disabled> No items </Dropdown.Item>
        ) : (
          items.map((item) => (
            <Dropdown.Item
              className={style.item}
              key={item}
              onClick={() => onSelect?.(item)}
            >
              {item}
            </Dropdown.Item>
          ))
        )}
      </Dropdown.Menu>
    </Dropdown>
  );
}
