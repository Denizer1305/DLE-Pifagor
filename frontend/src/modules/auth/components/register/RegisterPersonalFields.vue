<script setup lang="ts">
import type {
    RegisterFormErrors,
    RegisterFormState,
    RegistrationRole,
} from "@/modules/auth/types/auth-form.types";

interface Props {
    form: RegisterFormState;
    errors: RegisterFormErrors;
    role: RegistrationRole;
}

defineProps<Props>();
</script>

<template>
    <div class="form-grid">
        <div class="form-group">
            <label class="form-label" for="lastName">
                Фамилия
            </label>

            <input
                id="lastName"
                v-model="form.lastName"
                class="form-input"
                :class="{ 'is-invalid': errors.lastName }"
                type="text"
                autocomplete="family-name"
                placeholder="Иванов"
            />

            <p v-if="errors.lastName" class="form-error form-error--compact">
                Проверьте фамилию
            </p>
        </div>

        <div class="form-group">
            <label class="form-label" for="firstName">
                Имя
            </label>

            <input
                id="firstName"
                v-model="form.firstName"
                class="form-input"
                :class="{ 'is-invalid': errors.firstName }"
                type="text"
                autocomplete="given-name"
                placeholder="Иван"
            />

            <p v-if="errors.firstName" class="form-error form-error--compact">
                Проверьте имя
            </p>
        </div>
    </div>

    <div class="form-grid">
        <div class="form-group">
            <label class="form-label" for="middleName">
                Отчество
            </label>

            <input
                id="middleName"
                v-model="form.middleName"
                class="form-input"
                type="text"
                autocomplete="additional-name"
                placeholder="Иванович"
            />
        </div>

        <div class="form-group">
            <label class="form-label" for="birthDate">
                Дата рождения
            </label>

            <input
                id="birthDate"
                v-model="form.birthDate"
                class="form-input"
                :class="{ 'is-invalid': errors.birthDate }"
                type="date"
                autocomplete="bday"
            />

            <p v-if="errors.birthDate" class="form-error form-error--compact">
                Проверьте дату рождения
            </p>
        </div>
    </div>
</template>