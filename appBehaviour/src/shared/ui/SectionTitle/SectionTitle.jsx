import Title from "../Title/Title";
import styles from "./SectionTitle.module.css"

function SectionTitle({children}) {
  return (
    <div className={`container ${styles.title}`}>
      <Title>{children}</Title>
    </div>
  );
}

export default SectionTitle
