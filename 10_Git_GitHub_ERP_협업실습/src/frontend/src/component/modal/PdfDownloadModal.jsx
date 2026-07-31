'use client';

import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Download } from 'lucide-react';

export default function PdfDownloadDialog({ open, setOpen, onConfirm }) {
	return (
		<Dialog open={open} onOpenChange={setOpen}>
			<DialogContent className="max-w-[600px] p-0 overflow-hidden rounded-[18px] border-0">
				<div className="flex flex-col items-center px-10 pt-10 pb-9 text-center">
					<div className="mb-6 flex h-[72px] w-[72px] items-center justify-center rounded-[18px] bg-[#EFF6FF] text-[#2563EB]">
						<Download size={34} strokeWidth={2.5} />
					</div>

					<DialogTitle className="text-[28px] font-bold text-[#111827]">
						PDF 다운로드
					</DialogTitle>

					<p className="mt-4 text-[22px] leading-[1.45] text-[#6B7280]">
						선택한 데이터를 PDF 파일로 다운로드합니다.
						<br />
						계속 진행하시겠습니까?
					</p>
				</div>

				<div className="grid grid-cols-2 border-t border-[#E5E7EB] px-7 py-6">
					<button
						type="button"
						onClick={() => setOpen(false)}
						className="h-[66px] rounded-[10px] border border-[#D1D5DB] text-[22px] font-bold text-[#374151]"
					>
						취소
					</button>

					<button
						type="button"
						onClick={onConfirm}
						className="h-[66px] rounded-[10px] bg-[#2563EB] text-[22px] font-bold text-white"
					>
						확인
					</button>
				</div>
			</DialogContent>
		</Dialog>
	);
}
