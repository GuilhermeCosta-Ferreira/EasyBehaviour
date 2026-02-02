import { useNavigate } from "react-router-dom";

import Button from "../../../shared/ui/Button/Button";
import SectionTitle from "../../../shared/ui/SectionTitle/SectionTitle";
import IOPannel from "../components/IOPannel/IOPannel";
import TablePicker from "../components/TablePicker/TablePicker";

function DBPage() {
  const navigate = useNavigate();

  return (
    <div>
      <SectionTitle>DB Access</SectionTitle>
      <IOPannel></IOPannel>
      <TablePicker></TablePicker>
      <Button className="container" onClick={() => navigate("/")}>Go Back</Button>


    </div>
  )
}

export default DBPage
