import DesktopApp from "./DesktopApp";
import MomirPage from "./MomirPage";
import MobilePrintPage from "./components/MobilePrintPage";

export default function App() {
  const path = window.location.pathname;

  if (path === "/mobile") {
    return <MobilePrintPage />;
  }

  if (path === "/momir") {
    return <MomirPage />;
  }

  return <DesktopApp />;
}
