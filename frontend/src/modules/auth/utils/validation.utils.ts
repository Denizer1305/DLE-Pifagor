export function isEmpty(value: string): boolean {
    return !value.trim();
}

export function isValidEmail(value: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

export function normalizeEmail(value: string): string {
    return value.trim().toLowerCase();
}

export function normalizeText(value: string): string {
    return value.trim();
}

export function normalizePhone(value: string): string {
    const digits = value.replace(/\D/g, "");

    if (!digits) {
        return "";
    }

    if (digits.startsWith("8")) {
        return `+7${digits.slice(1)}`;
    }

    if (digits.startsWith("7")) {
        return `+${digits}`;
    }

    return `+7${digits}`;
}

export function isValidRussianPhone(value: string): boolean {
    return /^\+7\d{10}$/.test(normalizePhone(value));
}