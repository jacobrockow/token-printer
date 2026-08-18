import DesktopApp from "./DesktopApp";
import MobilePrintPage from "./components/MobilePrintPage";

export default function App() {
  const path = window.location.pathname;

  if (path === "/mobile") {
    return <MobilePrintPage />;
  }

  return <DesktopApp />;
}