<script setup lang="ts">
import { watch } from "vue";

import { usePhoneMask } from "@/modules/auth/composables/usePhoneMask";
import type {
    RegisterFormErrors,
    RegisterFormState,
} from "@/modules/auth/types/auth-form.types";

interface Props {
    form: RegisterFormState;
    errors: RegisterFormErrors;
}

const props = defineProps<Props>();

const {
    phone,
    handlePhoneInput,
    setPhone,
} = usePhoneMask(props.form.phone);

watch(
    () => props.form.phone,
    (value) => {
        if (value !== phone.value) {
            setPhone(value);
        }
    },
);

watch(phone, (value) => {
    props.form.phone = value;
});
</script>

<template>
    <div class="form-grid">
        <div class="form-group">
            <label
                class="form-label"
                for="registerEmail"
            >
                Email
            </label>

            <input
                id="registerEmail"
                v-model="form.email"
                class="form-input"
                :class="{ 'is-invalid': errors.email }"
                type="text"
                inputmode="email"
                autocomplete="email"
                placeholder="name@example.com"
            />

            <p
                v-if="errors.email"
                class="form-error"
            >
                {{ errors.email }}
            </p>
        </div>

        <div class="form-group">
            <label
                class="form-label"
                for="phone"
            >
                Телефон
            </label>

            <input
                id="phone"
                :value="phone"
                class="form-input"
                :class="{ 'is-invalid': errors.phone }"
                type="tel"
                inputmode="tel"
                autocomplete="tel"
                placeholder="+7 900 000-00-00"
                maxlength="16"
                @input="handlePhoneInput"
            />

            <p
                v-if="errors.phone"
                class="form-error"
            >
                {{ errors.phone }}
            </p>
        </div>
    </div>
</template>