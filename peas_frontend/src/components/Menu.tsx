import { Button, MegaMenu, Navbar } from "flowbite-react";

const Menu: React.FC = () => {
  return (
    <MegaMenu>
      <div className="mx-auto flex max-w-screen-xl flex-wrap items-center justify-between p-4 md:space-x-8">
        <Navbar.Brand href="/">
          <img alt="" src="/peas.svg" className="mr-3 h-6 sm:h-10" />
          <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
            Peas
          </span>
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse>
          <Navbar.Link href="/products">Products</Navbar.Link>
          <Navbar.Link href="/recipes">Recipes</Navbar.Link>
        </Navbar.Collapse>
      </div>
    </MegaMenu>
  );
};

export default Menu;