<script setup lang="ts">
import OrganizationActionMenu from "../shared/OrganizationActionMenu.vue";
import OrganizationPublicBadge from "./OrganizationPublicBadge.vue";
import OrganizationStatusBadge from "../shared/OrganizationStatusBadge.vue";

import type {
    OrganizationListItemView,
    OrganizationTableAction,
    OrganizationTableActionKey,
    OrganizationTableColumn,
} from "../../types";

interface Props {
    items: OrganizationListItemView[];
    columns: OrganizationTableColumn[];
    actions: OrganizationTableAction[];
    disabledActions?: Partial<Record<number, OrganizationTableActionKey[]>>;
}

interface Emits {
    (event: "select", item: OrganizationListItemView): void;
    (
        event: "action",
        payload: {
            actionKey: OrganizationTableActionKey;
            item: OrganizationListItemView;
        },
    ): void;
}

const props = withDefaults(defineProps<Props>(), {
    disabledActions: () => ({}),
});

defineEmits<Emits>();

function getDisabledActions(item: OrganizationListItemView): OrganizationTableActionKey[] {
    return props.disabledActions[item.id] ?? [];
}
</script>

<template>
    <section class="org-table">
        <div class="org-table__scroll">
            <table class="org-table__table">
                <thead class="org-table__head">
                    <tr class="org-table__row">
                        <th
                            v-for="column in columns"
                            :key="column.key"
                            class="org-table__cell org-table__cell--head"
                            :class="{
                                'org-table__cell--actions': column.key === 'actions',
                                'org-table__cell--compact': column.width,
                            }"
                            :style="{ width: column.width }"
                        >
                            {{ column.label }}
                        </th>
                    </tr>
                </thead>

                <tbody class="org-table__body">
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="org-table__row"
                    >
                        <td
                            class="org-table__cell"
                            data-label="Организация"
                        >
                            <button
                                class="org-table__entity"
                                type="button"
                                @click="$emit('select', item)"
                            >
                                <span class="org-table__avatar">
                                    <img
                                        v-if="item.logoUrl"
                                        :src="item.logoUrl"
                                        :alt="item.title"
                                    />
                                    <span v-else>
                                        {{ item.title.slice(0, 2).toUpperCase() }}
                                    </span>
                                </span>

                                <span class="org-table__entity-content">
                                    <span class="org-table__title">
                                        {{ item.title }}
                                    </span>

                                    <span class="org-table__subtitle">
                                        {{ item.subtitle }}
                                    </span>

                                    <span class="org-table__meta">
                                        <span
                                            v-for="metaItem in item.meta"
                                            :key="metaItem"
                                            class="org-table__meta-item"
                                        >
                                            {{ metaItem }}
                                        </span>
                                    </span>
                                </span>
                            </button>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Город"
                        >
                            {{ item.city }}
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Контакты"
                        >
                            <span class="org-table__subtitle">
                                {{ item.email }}
                            </span>

                            <span class="org-table__subtitle">
                                {{ item.phone }}
                            </span>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Статус"
                        >
                            <OrganizationStatusBadge :status="item.status" />

                            <OrganizationPublicBadge
                                :is-public="item.isPublic"
                                :is-default-public="item.isDefaultPublic"
                            />
                        </td>

                        <td
                            class="org-table__cell org-table__cell--actions"
                            data-label="Действия"
                        >
                            <OrganizationActionMenu
                                :actions="actions"
                                :disabled-actions="getDisabledActions(item)"
                                @action="
                                    $emit('action', {
                                        actionKey: $event,
                                        item,
                                    })
                                "
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>
