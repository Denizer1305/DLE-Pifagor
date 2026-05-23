import { nextTick, onBeforeUnmount, onMounted } from "vue";

interface UseScrollRevealOptions {
    selector?: string;
    visibleClass?: string;
    rootMargin?: string;
    threshold?: number;
}

export function useScrollReveal(options: UseScrollRevealOptions = {}) {
    const selector = options.selector ?? ".fade-in";
    const visibleClass = options.visibleClass ?? "visible";
    const rootMargin = options.rootMargin ?? "0px 0px -8% 0px";
    const threshold = options.threshold ?? 0.08;

    let observer: IntersectionObserver | null = null;

    function revealElements(): void {
        const elements = Array.from(document.querySelectorAll<HTMLElement>(selector));

        if (!elements.length) {
            return;
        }

        if (!("IntersectionObserver" in window)) {
            elements.forEach((element) => {
                element.classList.add(visibleClass);
            });

            return;
        }

        observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) {
                        return;
                    }

                    const element = entry.target as HTMLElement;

                    element.classList.add(visibleClass);
                    observer?.unobserve(element);
                });
            },
            {
                root: null,
                rootMargin,
                threshold,
            },
        );

        elements.forEach((element) => {
            if (element.classList.contains(visibleClass)) {
                return;
            }

            observer?.observe(element);
        });
    }

    onMounted(async () => {
        await nextTick();
        revealElements();
    });

    onBeforeUnmount(() => {
        observer?.disconnect();
        observer = null;
    });

    return {
        revealElements,
    };
}
