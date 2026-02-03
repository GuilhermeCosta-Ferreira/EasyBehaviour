import Button from "../../../../shared/ui/Button/Button";
import { useNavigate } from "react-router-dom";
import styles from "./HomePannel.module.css"

function HomePannel() {
  const navigate = useNavigate();

  return (
    <div className={`container ${styles.pannel}`}>
      <Button className={styles.pannelbutton} onClick={() => navigate("dlc_support")}>DLC Support</Button>
      <Button className={styles.pannelbutton} onClick={() => navigate("db_access")}>Check DB</Button>
      <Button className={styles.pannelbutton} onClick={() => navigate("analyze")}>Analyze Data</Button>
    </div>
  );
}

export default HomePannel
