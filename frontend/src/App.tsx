import DesktopApp from "./DesktopApp";
import MomirPage from "./MomirPage";
import AppNav from "./components/AppNav";
import MobilePrintPage from "./components/MobilePrintPage";
import "./styles/navigation.css";

export default function App() {
  const path = window.location.pathname;

  if (path === "/mobile") {
    return <MobilePrintPage />;
  }

  return (
    <>
      <AppNav />
      {path === "/momir" ? <MomirPage /> : <DesktopApp />}
    </>
  );
}
