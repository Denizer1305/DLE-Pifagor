import { useRouter } from "vue-router";

export function useSmoothScroll() {
    const router = useRouter();

    async function scrollToTop(): Promise<void> {
        window.scrollTo({
            top: 0,
            behavior: "smooth",
        });
    }

    async function goToRoute(routeName: string): Promise<void> {
        await router.push({
            name: routeName,
        });

        await scrollToTop();
    }

    function scrollToElement(selector: string): void {
        const element = document.querySelector(selector);

        if (!element) {
            return;
        }

        element.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
    }

    return {
        scrollToTop,
        goToRoute,
        scrollToElement,
    };
}
