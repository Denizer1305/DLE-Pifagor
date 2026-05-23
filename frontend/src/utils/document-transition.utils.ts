const DOCUMENT_TRANSITION_DURATION = 340;

export function runDocumentTransition(className: string): void {
    if (typeof window === "undefined" || typeof document === "undefined") {
        return;
    }

    const root = document.documentElement;
    const body = document.body;

    root.classList.add(className);
    body?.classList.add(className);

    window.setTimeout(() => {
        root.classList.remove(className);
        body?.classList.remove(className);
    }, DOCUMENT_TRANSITION_DURATION);
}
