import { useNavigate } from "react-router-dom";

import Button from "../../../shared/ui/Button/Button";
import SectionTitle from "../../../shared/ui/SectionTitle/SectionTitle";

function DBPage() {
  const navigate = useNavigate();

  return (
    <div>
      <SectionTitle>DB Access</SectionTitle>
      <Button className="container" onClick={() => navigate("/")}>Go Back</Button>
    </div>
  )
}

export default DBPage
