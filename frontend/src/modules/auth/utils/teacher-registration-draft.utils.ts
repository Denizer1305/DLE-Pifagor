import type { TeacherRegistrationPayload } from "@/modules/auth/types/auth.types";

const TEACHER_DRAFT_STORAGE_KEY = "pifagor.teacher.registration.draft";

export function saveTeacherRegistrationDraft(
    payload: Omit<TeacherRegistrationPayload, "invite_code">,
): void {
    window.sessionStorage.setItem(
        TEACHER_DRAFT_STORAGE_KEY,
        JSON.stringify(payload),
    );
}

export function getTeacherRegistrationDraft(): Omit<TeacherRegistrationPayload, "invite_code"> | null {
    const rawValue = window.sessionStorage.getItem(TEACHER_DRAFT_STORAGE_KEY);

    if (!rawValue) {
        return null;
    }

    try {
        return JSON.parse(rawValue) as Omit<TeacherRegistrationPayload, "invite_code">;
    } catch {
        return null;
    }
}

export function clearTeacherRegistrationDraft(): void {
    window.sessionStorage.removeItem(TEACHER_DRAFT_STORAGE_KEY);
}
