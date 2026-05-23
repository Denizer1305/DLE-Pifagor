import { computed, ref } from "vue";

const RUSSIAN_PHONE_PREFIX = "+7";
const MAX_PHONE_DIGITS = 11;

function onlyDigits(value: string): string {
    return value.replace(/\D/g, "");
}

function normalizeRussianPhoneDigits(value: string): string {
    let digits = onlyDigits(value);

    if (!digits) {
        return "";
    }

    if (digits.startsWith("8")) {
        digits = `7${digits.slice(1)}`;
    }

    if (!digits.startsWith("7")) {
        digits = `7${digits}`;
    }

    return digits.slice(0, MAX_PHONE_DIGITS);
}

export function formatRussianPhone(value: string): string {
    const digits = normalizeRussianPhoneDigits(value);

    if (!digits) {
        return "";
    }

    const withoutCountry = digits.startsWith("7")
        ? digits.slice(1)
        : digits;

    let result = RUSSIAN_PHONE_PREFIX;

    if (withoutCountry.length > 0) {
        result += ` ${withoutCountry.slice(0, 3)}`;
    }

    if (withoutCountry.length > 3) {
        result += ` ${withoutCountry.slice(3, 6)}`;
    }

    if (withoutCountry.length > 6) {
        result += `-${withoutCountry.slice(6, 8)}`;
    }

    if (withoutCountry.length > 8) {
        result += `-${withoutCountry.slice(8, 10)}`;
    }

    return result;
}

export function normalizeRussianPhone(value: string): string {
    const digits = normalizeRussianPhoneDigits(value);

    if (!digits) {
        return "";
    }

    return `+${digits}`;
}

export function isRussianPhoneComplete(value: string): boolean {
    return normalizeRussianPhone(value).length === 12;
}

export function usePhoneMask(initialValue = "") {
    const phone = ref(formatRussianPhone(initialValue));

    const normalizedPhone = computed(() => {
        return normalizeRussianPhone(phone.value);
    });

    const isPhoneComplete = computed(() => {
        return isRussianPhoneComplete(phone.value);
    });

    function setPhone(value: string): void {
        phone.value = formatRussianPhone(value);
    }

    function handlePhoneInput(event: Event): void {
        const input = event.target as HTMLInputElement;

        phone.value = formatRussianPhone(input.value);
    }

    function clearPhone(): void {
        phone.value = "";
    }

    return {
        phone,
        normalizedPhone,
        isPhoneComplete,
        setPhone,
        handlePhoneInput,
        clearPhone,
    };
}
