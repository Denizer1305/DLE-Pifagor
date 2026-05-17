import { onBeforeUnmount, onMounted, ref } from "vue";

interface UseScrollHeaderOptions {
    threshold?: number;
}

export function useScrollHeader(options: UseScrollHeaderOptions = {}) {
    const threshold = options.threshold ?? 24;

    const isScrolled = ref(false);

    function updateScrollState(): void {
        isScrolled.value = window.scrollY > threshold;
    }

    onMounted(() => {
        updateScrollState();

        window.addEventListener("scroll", updateScrollState, {
            passive: true,
        });
    });

    onBeforeUnmount(() => {
        window.removeEventListener("scroll", updateScrollState);
    });

    return {
        isScrolled,
    };
}