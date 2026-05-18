import { nextTick } from "vue";

export function useAuthPageMotion() {
    async function revealPage(): Promise<void> {
        await nextTick();

        window.requestAnimationFrame(() => {
            document
                .querySelectorAll<HTMLElement>(".auth-page .fade-in")
                .forEach((element, index) => {
                    element.style.transitionDelay = `${index * 90}ms`;
                    element.classList.add("visible");
                });
        });
    }

    return {
        revealPage,
    };
}
