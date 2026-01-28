import Title from "../../../../shared/ui/Title/Title";
import Description from "../../../../shared/ui/Description/Description";
import styles from "./HomeTitle.module.css";

function HomeTitle() {
  return (
    <div className={`container ${styles.hometitle}`}>
      <Title>EasyBehaviour</Title>
      <Description>The best tool for analysing your study's behaviour data</Description>
    </div>
  );
}

export default HomeTitle
