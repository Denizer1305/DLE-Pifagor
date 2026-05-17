<script setup lang="ts">
import type {
    RegisterFormErrors,
    RegisterFormState,
} from "@/modules/auth/types/auth-form.types";

interface Props {
    form: RegisterFormState;
    errors: RegisterFormErrors;
}

defineProps<Props>();
</script>

<template>
    <div class="form-group full">
        <label
            class="form-label"
            for="inviteCode"
        >
            Код организации
        </label>

        <input
            id="inviteCode"
            v-model="form.inviteCode"
            class="form-input"
            :class="{ 'is-invalid': errors.inviteCode }"
            type="text"
            placeholder="Введите код образовательной организации"
        />

        <p
            v-if="errors.inviteCode"
            class="form-error"
        >
            {{ errors.inviteCode }}
        </p>

        <p class="form-hint">
            Код выдаёт образовательная организация. После регистрации заявка уйдёт администратору, 
            директору или заведующему отделением на проверку.
        </p>
    </div>
</template>