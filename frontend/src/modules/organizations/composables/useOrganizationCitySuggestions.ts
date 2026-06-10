import { ref } from "vue";

import { getProfileCitySuggestions } from "@/modules/profile/services/profile-edit.service";
import type { ProfileCitySuggestion } from "@/modules/profile/types/profile-edit.types";

const MIN_CITY_QUERY_LENGTH = 2;
const CITY_SEARCH_DELAY = 250;

export function useOrganizationCitySuggestions() {
    const citySuggestions = ref<ProfileCitySuggestion[]>([]);
    const isCitySuggestionsLoading = ref(false);
    let requestId = 0;
    let searchTimer: ReturnType<typeof setTimeout> | null = null;

    function searchCities(query: string): void {
        const normalizedQuery = query.trim();

        if (searchTimer) {
            clearTimeout(searchTimer);
        }

        if (normalizedQuery.length < MIN_CITY_QUERY_LENGTH) {
            citySuggestions.value = [];
            isCitySuggestionsLoading.value = false;
            return;
        }

        searchTimer = setTimeout(async () => {
            const currentRequestId = ++requestId;

            isCitySuggestionsLoading.value = true;

            try {
                const suggestions = await getProfileCitySuggestions(normalizedQuery);

                if (currentRequestId === requestId) {
                    citySuggestions.value = suggestions;
                }
            } catch {
                if (currentRequestId === requestId) {
                    citySuggestions.value = [];
                }
            } finally {
                if (currentRequestId === requestId) {
                    isCitySuggestionsLoading.value = false;
                }
            }
        }, CITY_SEARCH_DELAY);
    }

    function clearCitySuggestions(): void {
        if (searchTimer) {
            clearTimeout(searchTimer);
            searchTimer = null;
        }

        citySuggestions.value = [];
        isCitySuggestionsLoading.value = false;
    }

    return {
        citySuggestions,
        isCitySuggestionsLoading,
        clearCitySuggestions,
        searchCities,
    };
}
