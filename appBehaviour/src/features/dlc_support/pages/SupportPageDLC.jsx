import { useNavigate } from "react-router-dom";
import Button from "../../../shared/ui/Button/Button"
import SupportTitle from "../components/SupportTitle/SupportTitle";

function SupportPageDLC() {
  const navigate = useNavigate();

  return (
    <div>
      <SupportTitle>DLC Support</SupportTitle>
      <Button className="container" onClick={() => navigate("/")}>Go Back</Button>
    </div>
  )
}

export default SupportPageDLC
