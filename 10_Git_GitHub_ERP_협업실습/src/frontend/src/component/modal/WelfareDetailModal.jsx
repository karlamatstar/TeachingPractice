'use client';
import axios from 'axios';

import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
} from '@/components/ui/dialog';
import {
	Gift,
	X,
	Calendar,
	User,
	MapPin,
	CreditCard,
	Clock,
	FileText,
	Download,
	MessageSquare,
} from 'lucide-react';
import LoadingSpinner from '@/common/LoadingSpinner';
import c from './WelfareDetailModal.module.css';
import clsx from 'clsx';
import { parsingDate } from '@/common/utils/dateUtils';
import { getSizeMB } from '@/common/utils/fileUtil';

export default function WelfareDetailModal({
	open,
	setOpen,
	isLoading,
	detailInfo = {},
}) {
	const goDownloadFile = async () => {
		const token = localStorage.getItem('accessToken');

		const res = await axios.get(
			`http://localhost:33000/api/v1/files/${detailInfo?.savedFileId}/download`,
			{
				responseType: 'blob',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			}
		);

		const url = window.URL.createObjectURL(res?.data);

		const a = document.createElement('a');
		a.href = url;
		a.download = detailInfo?.savedFileName; // 원본 파일명
		document.body.appendChild(a);
		a.click();
		a.remove();
		window.URL.revokeObjectURL(url);
	};

	return (
		<Dialog open={open} onOpenChange={setOpen}>
			<DialogContent className="max-w-[520px] !p-0 overflow-hidden rounded-[10px]">
				{/* Header */}
				<DialogHeader className="bg-[#1E3F73] text-white !px-5 !py-4">
					<div className="flex items-center justify-between">
						<div className="flex items-center gap-3">
							<Gift size={18} />
							<div>
								<DialogTitle className="text-[16px] font-bold">
									경조비 신청 상세
								</DialogTitle>
								<p className="text-[11px] text-blue-100">
									Welfare Benefit Detail
								</p>
							</div>
						</div>

						<div className="flex items-center gap-2">
							<span className="rounded-full bg-[#D99A00] !px-3 !py-1 text-[12px] font-bold">
								검토중
							</span>
							{/* <button
								onClick={() => setOpen(false)}
								className="rounded bg-white/15 p-1 hover:bg-white/25"
							>
								<X size={18} />
							</button> */}
						</div>
					</div>
				</DialogHeader>

				<div className={clsx('!p-5 space-y-5 bg-white', c.contentWrapper)}>
					{/* 신청 정보 */}
					<div className="rounded-lg border bg-[#F8FAFC] !p-4">
						<div className="flex justify-between text-[12px] text-gray-500 mb-3">
							<span># 신청번호: WEL-2025-07-001</span>
							<span className="flex items-center gap-1">
								<Calendar size={13} /> 신청일:{' '}
								{detailInfo?.applicationDate || '신청일 확인 불가'}
							</span>
						</div>

						<div
							className={clsx(
								'flex items-center justify-between text-[11px]',
								c.statusWrapper
							)}
						>
							{['신청완료', '검토중', '승인', '지급완료'].map((item, idx) => (
								<div
									key={item}
									className={clsx(
										'flex flex-col items-center flex-1',
										c.statusItem
									)}
								>
									<div
										className={`w-5 h-5 rounded-full flex items-center justify-center text-white ${
											idx === 0
												? 'bg-[#1E3F73]'
												: idx === 1
													? 'bg-[#D99A00]'
													: 'bg-gray-300'
										}`}
									>
										{idx === 0 ? '✓' : ''}
									</div>
									<span
										className={`mt-1 ${
											idx === 1 ? 'text-[#D99A00] font-bold' : 'text-gray-400'
										}`}
									>
										{item}
									</span>
								</div>
							))}
						</div>
					</div>

					<Section title="경조 정보">
						<InfoRow label="경조구분">
							<span className="text-pink-500 font-bold">
								{detailInfo?.eventType}
							</span>
							<span className="ml-3 text-gray-400">
								경조비 지급 규정 3조 1항
							</span>
						</InfoRow>
						<InfoRow label="대상자 / 관계">
							<span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-pink-100 text-pink-500 text-[12px] font-bold mr-2">
								{(detailInfo?.targetName || '').slice(0, 1)}
							</span>
							<b>{detailInfo?.targetName}</b>
							<span className="ml-2 rounded bg-gray-100 !px-2 !py-1 text-[11px]">
								{detailInfo?.familyRelation}
							</span>
						</InfoRow>
						<InfoRow label="경조일">
							<Calendar size={14} /> 2025년 7월 20일 (일)
						</InfoRow>
						<InfoRow label="경조 장소">
							<MapPin size={14} /> 더케이서울호텔 그랜드볼룸
						</InfoRow>
					</Section>

					<Section title="지급 정보">
						<InfoRow label="지급금액">
							<CreditCard size={14} />
							<b className="text-[#1E3F73] text-[16px]">{`${detailInfo?.requestedAmount}원`}</b>
							{/* <span className="text-gray-400">(오십만원정)</span> */}
						</InfoRow>
						<InfoRow label="지급계좌">
							<CreditCard size={14} />{' '}
							{`${detailInfo?.bankName} ${detailInfo?.accountNumber} (${detailInfo?.accountHolder})`}{' '}
						</InfoRow>
						<InfoRow label="예상 지급일">
							<Clock size={14} /> 승인 후 3영업일 이내
						</InfoRow>
					</Section>

					{detailInfo?.savedFileName && (
						<Section title="첨부 서류">
							<FileItem
								name={detailInfo?.savedFileName}
								type={`${detailInfo?.savedFileExt} · ${getSizeMB(detailInfo?.savedFileSize)} MB · ${parsingDate(detailInfo?.savedFileDate)} 업로드`}
								goDownloadFile={goDownloadFile}
							/>
						</Section>
					)}

					<Section title="검토 의견" yellow>
						<div className="rounded-lg border border-yellow-300 bg-yellow-50 !p-3 text-[13px] text-[#B36B00]">
							<div className="flex gap-2 font-bold">
								<MessageSquare size={15} />
								서류 확인 중입니다. 추가 서류 제출이 필요할 수 있습니다.
							</div>
							<p className="mt-1 ml-6 text-[12px]">
								검토자: 김인사 (인사팀장) · 2025.07.02
							</p>
						</div>
					</Section>
				</div>

				{/* Footer */}
				<div className="flex items-center justify-between border-t bg-[#F8FAFC] !px-5 !py-3">
					<span className="text-[12px] text-gray-400">
						ⓘ 최종 수정: 2025.07.02 · 인사팀
					</span>

					<div className="flex gap-2">
						<button className="rounded-md border border-red-200 !px-4 !py-2 text-[13px] font-bold text-red-500 cursor-pointer">
							× 신청취소
						</button>
						<button
							onClick={() => setOpen(false)}
							className="rounded-md bg-[#1E3F73] !px-4 !py-2 text-[13px] font-bold text-white cursor-pointer"
						>
							× 닫기
						</button>
					</div>
				</div>
				<LoadingSpinner isLoading={isLoading} />
			</DialogContent>
		</Dialog>
	);
}

function Section({ title, children, yellow }) {
	return (
		<section className={clsx('!mt-[10px]', c.sectionWrapper)}>
			<h3
				className={`mb-3 border-l-4 pl-2 text-[15px] font-bold ${
					yellow
						? 'border-yellow-500 text-yellow-600'
						: 'border-[#1E3F73] text-[#1E3F73]'
				} ${c.title}`}
			>
				{title}
			</h3>
			<div>{children}</div>
		</section>
	);
}

function InfoRow({ label, children }) {
	return (
		<div className="grid grid-cols-[120px_1fr] border-b text-[13px] last:border-b-0">
			<div className="bg-gray-50 !px-4 !py-3 font-bold text-gray-500">
				{label}
			</div>
			<div className="flex items-center gap-2 !px-4 !py-3 text-gray-700">
				{children}
			</div>
		</div>
	);
}

function FileItem({ name, type, red, goDownloadFile }) {
	return (
		<div className="flex items-center justify-between border-b !py-3 last:border-b-0">
			<div className="flex items-center gap-3">
				<div
					className={`flex h-8 w-8 items-center justify-center rounded ${
						red ? 'bg-red-50 text-red-500' : 'bg-blue-50 text-blue-500'
					}`}
				>
					<FileText size={17} />
				</div>
				<div>
					<p className="text-[13px] font-bold text-gray-700">{name}</p>
					<p className="text-[12px] text-gray-400">{type}</p>
				</div>
			</div>
			<button
				className="text-gray-400 hover:text-gray-600"
				onClick={() => goDownloadFile()}
			>
				<Download size={16} />
			</button>
		</div>
	);
}
