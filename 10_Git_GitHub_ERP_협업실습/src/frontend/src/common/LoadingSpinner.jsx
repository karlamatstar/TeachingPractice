'use client';

import {Spinner} from "@/components/ui/spinner";

export default function LoadingSpinner({isLoading = false}) {
	return (
		<>
			{isLoading ? (
				<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
					<Spinner className="size-8"/>
				</div>
			) : null}
		</>
	);
}