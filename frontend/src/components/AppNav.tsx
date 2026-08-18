export default function AppNav() {
  const path = window.location.pathname;

  return (
    <nav className="app-global-nav" aria-label="Application pages">
      <a href="/" aria-current={path === "/" ? "page" : undefined}>
        Token Search
      </a>
      <a href="/momir" aria-current={path === "/momir" ? "page" : undefined}>
        Momir
      </a>
    </nav>
  );
}
