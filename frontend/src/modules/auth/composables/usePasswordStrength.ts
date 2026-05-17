import { computed, type Ref } from "vue";

export interface PasswordChecks {
    length: boolean;
    upper: boolean;
    digit: boolean;
}

export interface PasswordStrengthResult {
    checks: PasswordChecks;
    score: number;
    label: string;
    width: string;
    isValid: boolean;
}

export function evaluatePasswordStrength(password: string): PasswordStrengthResult {
    const checks: PasswordChecks = {
        length: password.length >= 8,
        upper: /[A-ZА-ЯЁ]/.test(password),
        digit: /\d/.test(password),
    };

    const score = Object.values(checks).filter(Boolean).length;

    let label = "Недостаточно";

    if (score === 1) {
        label = "Слабый";
    }

    if (score === 2) {
        label = "Средний";
    }

    if (score === 3) {
        label = "Надёжный";
    }

    return {
        checks,
        score,
        label,
        width: `${Math.round((score / 3) * 100)}%`,
        isValid: score === 3,
    };
}

export function usePasswordStrength(password: Ref<string>) {
    const strength = computed(() => {
        return evaluatePasswordStrength(password.value);
    });

    const checks = computed(() => {
        return strength.value.checks;
    });

    const score = computed(() => {
        return strength.value.score;
    });

    const label = computed(() => {
        return strength.value.label;
    });

    const width = computed(() => {
        return strength.value.width;
    });

    const isValid = computed(() => {
        return strength.value.isValid;
    });

    return {
        strength,
        checks,
        score,
        label,
        width,
        isValid,
    };
}