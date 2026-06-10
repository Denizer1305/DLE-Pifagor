<script setup lang="ts">
import type {
    OrganizationEntityKey,
    OrganizationNavigationItem,
} from "../../types";

interface Props {
    items: OrganizationNavigationItem[];
    activeKey: OrganizationEntityKey;
    title?: string;
}

interface Emits {
    (event: "select", key: OrganizationEntityKey): void;
}

withDefaults(defineProps<Props>(), {
    title: "",
});

defineEmits<Emits>();
</script>

<template>
    <nav class="org-admin-nav">
        <p
            v-if="title"
            class="org-admin-nav__title"
        >
            {{ title }}
        </p>

        <ul class="org-admin-nav__list">
            <li
                v-for="item in items"
                :key="item.key"
                class="org-admin-nav__item"
            >
                <button
                    class="org-admin-nav__link"
                    :class="{ 'is-active': item.key === activeKey }"
                    type="button"
                    @click="$emit('select', item.key)"
                >
                    <span class="org-admin-nav__icon">
                        <slot
                            name="icon"
                            :icon="item.icon"
                            :item="item"
                        >
                            {{ item.icon }}
                        </slot>
                    </span>

                    <span class="org-admin-nav__content">
                        <span class="org-admin-nav__label">
                            {{ item.label }}
                        </span>

                        <span
                            v-if="item.hint"
                            class="org-admin-nav__hint"
                        >
                            {{ item.hint }}
                        </span>
                    </span>

                    <span
                        v-if="item.badge"
                        class="org-admin-nav__badge"
                    >
                        {{ item.badge }}
                    </span>
                </button>
            </li>
        </ul>
    </nav>
</template>