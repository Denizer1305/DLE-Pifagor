import { computed, type Ref } from "vue";

import {
    evaluatePasswordStrength,
    type PasswordChecks,
    type PasswordStrength,
} from "@/modules/auth/utils/password.utils";

export { evaluatePasswordStrength };
export type { PasswordChecks, PasswordStrength };
export type PasswordStrengthResult = PasswordStrength;

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
