export interface PasswordChecks {
    length: boolean;
    upper: boolean;
    digit: boolean;
}

export interface PasswordStrength {
    checks: PasswordChecks;
    score: number;
    label: string;
    width: string;
    isValid: boolean;
}

export function evaluatePasswordStrength(password: string): PasswordStrength {
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
