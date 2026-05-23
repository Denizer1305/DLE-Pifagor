<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import { evaluatePasswordStrength } from "@/modules/auth/composables/usePasswordStrength";

interface Props {
    password: string;
    passwordConfirm?: string;
    showMatchRule?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
    passwordConfirm: "",
    showMatchRule: false,
});
const { tr } = useI18n();

const strength = computed(() => {
    return evaluatePasswordStrength(props.password);
});

const passwordsMatch = computed(() => {
    if (!props.showMatchRule) {
        return true;
    }

    return Boolean(
        props.password &&
        props.passwordConfirm &&
        props.password === props.passwordConfirm,
    );
});

const rules = computed(() => {
    const baseRules = [
        {
            key: "length",
            label: "Минимум 8 символов",
            isValid: strength.value.checks.length,
        },
        {
            key: "upper",
            label: "Хотя бы одна заглавная буква",
            isValid: strength.value.checks.upper,
        },
        {
            key: "digit",
            label: "Хотя бы одна цифра",
            isValid: strength.value.checks.digit,
        },
    ];

    if (props.showMatchRule) {
        baseRules.push({
            key: "match",
            label: "Пароли совпадают",
            isValid: passwordsMatch.value,
        });
    }

    return baseRules;
});
</script>

<template>
    <div class="password-hint">
        <div class="password-hint__top">
            <span class="password-hint__label">
                {{ tr("Требования к паролю") }}
            </span>

            <strong class="password-hint__value">
                {{ tr(strength.label) }}
            </strong>
        </div>

        <div class="password-hint__bar">
            <span
                class="password-hint__bar-fill"
                :style="{ width: strength.width }"
            ></span>
        </div>

        <ul class="password-hint__rules">
            <li
                v-for="rule in rules"
                :key="rule.key"
                class="password-hint__rule"
                :class="{ 'is-valid': rule.isValid }"
            >
                <i
                    :class="rule.isValid
                        ? 'fa-solid fa-check-circle'
                        : 'fa-regular fa-circle'"
                ></i>

                <span>{{ tr(rule.label) }}</span>
            </li>
        </ul>
    </div>
</template>
