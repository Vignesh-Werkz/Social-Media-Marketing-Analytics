export type SiteConfig = typeof siteConfig;

export const siteConfig = {
    name: "Datalyzer",
    description: "Make informed decisions through advanced data analysis.",
    navItems: [
        {
            label: "Home",
            href: "/",
        },
        {
            label: "Dashboard",
            href: "/dashboard",
        },
        {
            label: "Aggregates",
            href: "/aggregates",
        },
        {
            label: "About",
            href: "/about",
        },
    ],
    navMenuItems: [
        {
            label: "Profile",
            href: "/profile",
        },
        {
            label: "Dashboard",
            href: "/dashboard",
        },
        {
            label: "Projects",
            href: "/projects",
        },
        {
            label: "Team",
            href: "/team",
        },
        {
            label: "Calendar",
            href: "/calendar",
        },
        {
            label: "Settings",
            href: "/settings",
        },
        {
            label: "Help & Feedback",
            href: "/help-feedback",
        },
        {
            label: "Logout",
            href: "/logout",
        },
    ],
    links: {
        github: "https://github.com/nus-cs3203/24s1-open-project-team03",
        docs: "https://github.com/nus-cs3203/24s1-open-project-team03/wiki",
    },
};
