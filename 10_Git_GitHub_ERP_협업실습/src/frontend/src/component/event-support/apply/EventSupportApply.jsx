'use client';
import axios from 'axios';

import BreadCrumb from '@/component/common/BreadCrumb';
import MainTitleWrapper from '@/component/common/MainTitleWrapper';
import c from './EventSupportApply.module.css';
import {
	Baby,
	CakeSlice,
	CalendarDays,
	Ellipsis,
	Flower2,
	Heart,
	HeartHandshake,
	Info,
	Lock,
	Paperclip,
	Download,
	FileText,
	XIcon,
	SendHorizontal,
	UserPlus,
	Save,
	Gift,
	Clock7,
} from 'lucide-react';
import { Calendar } from '@/components/ui/calendar';

import { clsx } from 'clsx';
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from '@/components/ui/popover';

import { useEffect, useState, useRef } from 'react';
import CButton from '@/component/common/element/CButton';
import { getToday, parsingDate } from '@/common/utils/dateUtils';
import ViewTable from '@/component/common/ViewTable';
import {
	Dialog,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from '@/components/ui/dialog';
import LoadingSpinner from '@/common/LoadingSpinner';
import WelfareDetailModal from '@/component/modal/WelfareDetailModal';
import { getSizeMB } from '@/common/utils/fileUtil';
import { toast } from 'sonner';
import baseApi from '@/common/api/baseApi';

const bankList = [
	{ value: 'KB', label: 'KB국민은행' },
	{ value: 'SHINHAN', label: '신한은행' },
	{ value: 'WOORI', label: '우리은행' },
	{ value: 'HANA', label: '하나은행' },
	{ value: 'NH', label: 'NH농협은행' },
	{ value: 'IBK', label: 'IBK기업은행' },
	{ value: 'SC', label: 'SC제일은행' },
	{ value: 'CITI', label: '씨티은행' },
	{ value: 'KDB', label: 'KDB산업은행' },
	{ value: 'SUHYUP', label: '수협은행' },
	{ value: 'POST', label: '우체국' },
	{ value: 'MG', label: '새마을금고' },
	{ value: 'SHINHYUP', label: '신협' },
	{ value: 'KFCC', label: '저축은행' },
	{ value: 'KBANK', label: '케이뱅크' },
	{ value: 'KAKAO', label: '카카오뱅크' },
	{ value: 'TOSS', label: '토스뱅크' },
	{ value: 'BUSAN', label: '부산은행' },
	{ value: 'DAEGU', label: '대구은행' },
	{ value: 'GWANGJU', label: '광주은행' },
	{ value: 'JEONBUK', label: '전북은행' },
	{ value: 'GYEONGNAM', label: '경남은행' },
	{ value: 'JEJU', label: '제주은행' },
];

const relationList = [
	{ value: '본인', label: '본인' },
	{ value: '배우자', label: '배우자' },
	{ value: '부', label: '부' },
	{ value: '모', label: '모' },
	{ value: '조부', label: '조부' },
	{ value: '조모', label: '조모' },
	{ value: '외조부', label: '외조부' },
	{ value: '외조모', label: '외조모' },
	{ value: '자녀', label: '자녀' },
	{ value: '형제', label: '형제' },
	{ value: '자매', label: '자매' },
	{ value: '시부', label: '시부' },
	{ value: '시모', label: '시모' },
	{ value: '장인', label: '장인' },
	{ value: '장모', label: '장모' },
	{ value: '며느리', label: '며느리' },
	{ value: '사위', label: '사위' },
];

const columns = [
	'NO',
	'신청일',
	'경조구분',
	'대상자',
	'관계',
	'경조일',
	'지급금액',
	'지급계좌',
	'처리상태',
	'관리',
];

const dummyrowList = [
	{
		신청일: '2025.07.01',
		경조구분: '출산',
		대상자: '이동훈',
		관계: '본인',
		경조일: '2025.07.01',
		지급금액: '500,000원',
		지급계좌: '국민 12-****-****',
		처리상태: '검토중',
	},
	{
		신청일: '2025.06.28',
		경조구분: '결혼',
		대상자: '김민수',
		관계: '본인',
		경조일: '2025.07.10',
		지급금액: '1,000,000원',
		지급계좌: '신한 11-****-****',
		처리상태: '승인완료',
	},
	{
		신청일: '2025.06.25',
		경조구분: '부친상',
		대상자: '박지영',
		관계: '부친',
		경조일: '2025.06.24',
		지급금액: '700,000원',
		지급계좌: '우리 22-****-****',
		처리상태: '지급완료',
	},
	{
		신청일: '2025.06.20',
		경조구분: '모친상',
		대상자: '최현우',
		관계: '모친',
		경조일: '2025.06.19',
		지급금액: '700,000원',
		지급계좌: '하나 33-****-****',
		처리상태: '검토중',
	},
	{
		신청일: '2025.06.18',
		경조구분: '출산',
		대상자: '이수진',
		관계: '배우자',
		경조일: '2025.06.17',
		지급금액: '500,000원',
		지급계좌: '농협 44-****-****',
		처리상태: '반려',
	},
];

const smallFlexIndex = [2, 3, 4, 8, 9];

const getStatusClass = (item) => {
	const typeClass = {
		검토중: 'text-[#CA8A04] bg-[#FEF9C3]',
		승인완료: 'text-[#2563EB] bg-[#EFF6FF]',
		지급완료: 'text-[#166534] bg-[#DCFCE7]',
		반려: 'text-[#B91C1C] bg-[#FEE2E2]',
	};
	return `${typeClass[item] ?? 'text-[#6B7280] bg-[#F3F4F6]'} text-[11px] px-[10px] py-[3px] rounded-[8px] font-[700]`;
};

const getEventTypeClass = (item) => {
	const typeClass = {
		출산: 'text-[#16A34A] bg-[#F0FDF4]',
		결혼: 'text-[#2563EB] bg-[#EFF6FF]',
		본인결혼: 'text-[#2563EB] bg-[#DBEAFE]',
		부친상: 'text-[#DC2626] bg-[#FEF2F2]',
		모친상: 'text-[#DC2626] bg-[#FEF2F2]',
		배우자상: 'text-[#B91C1C] bg-[#FEE2E2]',
		조부상: 'text-[#EA580C] bg-[#FFF7ED]',
		조모상: 'text-[#EA580C] bg-[#FFF7ED]',
		칠순: 'text-[#7C3AED] bg-[#F3E8FF]',
		팔순: 'text-[#9333EA] bg-[#FAF5FF]',
		퇴직: 'text-[#475569] bg-[#F1F5F9]',
	};

	return `${typeClass[item] ?? 'text-[#6B7280] bg-[#F3F4F6]'} text-[11px] px-[10px] py-[3px] rounded-[8px] font-[700]`;
};

const eventTypeList = [
	{
		text: '본인결혼',
		icon: <Heart size={13} color="#D1D5DB" />,
	},
	{
		text: '자녀결혼',
		icon: <Heart size={13} color="#D1D5DB" />,
	},
	{
		text: '출산',
		icon: <Baby size={13} color="#D1D5DB" />,
	},
	{
		text: '부모사망',
		icon: <Flower2 size={13} color="#D1D5DB" />,
	},
	{
		text: '배우자사망',
		icon: <Flower2 size={13} color="#D1D5DB" />,
	},
	{
		text: '부모회갑',
		icon: <CakeSlice size={13} color="#D1D5DB" />,
	},
	{
		text: '기타',
		icon: <Ellipsis size={13} color="#D1D5DB" />,
	},
];

// "EmployeeEventSupportId": 1,
// "accountHolder": "이동훈",
// "accountNumber": "3120116768251",
// "applicationDate": "2026-06-18",
// "approvalStatus": "확인",
// "bankName": "농협",
// "employee_id": null,
// "eventDate": "2026-06-18",
// "eventLocation": "서울",
// "eventType": "결혼",
// "familyRelation": "본인",
// "memo": "string",
// "requestedAmount": 50000,
// "targetName": "이동훈"

const columnKeyMap = {
	신청일: 'applicationDate',
	경조구분: 'eventType',
	대상자: 'targetName',
	관계: 'familyRelation',
	경조일: 'eventDate',
	지급금액: 'requestedAmount',
	지급계좌: 'accountNumber',
	처리상태: '',
};

const initialApplyFormInfo = {
	relation: '',
	targetName: '',
	eventLocation: '',
	bankNumber: '',
	bankName: '',
	holderName: '',
};

export default function EventSupportApply() {
	const fileUploaderRef = useRef(null);
	const [openCalendar, setOpenCalendar] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [openDialog, setOpenDialog] = useState(false);
	const [date, setDate] = useState(parsingDate(new Date()));
	const [userInfo, setUserInfo] = useState({});
	const [selectedEventType, setSelectedEventType] = useState('본인결혼');
	const [applyFormInfo, setApplyFormInfo] = useState({});
	const [uploadedFileList, setUploadedFileList] = useState([]);
	const [uploadedFileId, setUploadedFileId] = useState(null);
	const [rowList, setRowList] = useState([]);
	const [modalDetailInfo, setModalDeatilInfo] = useState({});

	const getEventModalDetail = async (item) => {
		try {
			setIsLoading(true);
			const token = localStorage.getItem('accessToken');
			const res = await baseApi.get(
				`/api/v1/support/detail/${item.EmployeeEventSupportId}`,
				{
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);
			setModalDeatilInfo(res?.data?.data);
			setOpenDialog(true);
		} catch (e) {
		} finally {
			setIsLoading(false);
		}
	};

	const fileUpload = async (files) => {
		try {
			const formData = new FormData();
			for (const f of files) {
				formData.append('file', f);
				setUploadedFileList((prev) => [
					...prev,
					{
						fileSize: `${getSizeMB(f.size)}MB`,
						fileName: f.name,
					},
				]);
			}

			formData.append('refType', '경조사비신청');

			const token = localStorage.getItem('accessToken');

			const res = await axios.post(
				'http://localhost:33000/api/v1/files/upload',
				formData,
				{
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);

			setUploadedFileId(res?.data?.data);
			toast('파일업로드 성공');
		} catch (e) {
		} finally {
		}
	};

	const getAppliedHistory = async () => {
		const token = localStorage.getItem('accessToken');

		const res = await baseApi.get('/api/v1/support', {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});

		setRowList(res?.data?.data || []);
	};

	useEffect(() => {
		const jsonUser = localStorage.getItem('user');
		const parsedUserInfo = JSON.parse(jsonUser);
		setUserInfo({ ...parsedUserInfo });
	}, []);

	useEffect(() => {
		getAppliedHistory();
	}, []);

	const renderRow = (item, idx) => {
		return columns.map((c, cIdx) => {
			if (c === 'NO') {
				return (
					<li key={cIdx} className="flex-1 text-[12px] text-[#374151]">
						{idx}
					</li>
				);
			}

			if (c === '관리') {
				return (
					<li
						key={cIdx}
						className="flex-[0.5] text-[12px] text-[#374151]"
						onClick={async () => {
							await getEventModalDetail(item);
						}}
					>
						<span
							className={clsx(
								c.tableDetailButton,
								'text-[#374151] text-[12px] px-[10px] py-[4px] bg-[#F1F5F9] rounded-[4px]'
							)}
						>
							상세
						</span>
					</li>
				);
			}

			return (
				<li
					key={cIdx}
					className={clsx(
						['경조구분', '대상자', '관계', '처리상태'].includes(c)
							? 'flex-[0.5]'
							: 'flex-1',
						'text-[12px] text-[#374151]'
					)}
				>
					<span
						className={clsx(
							c === '경조구분' && getEventTypeClass(item[c]),
							c === '대상자' && 'font-[700]',
							c === '지급금액' && 'text-[#1B3A6B]',
							c === '처리상태' && getStatusClass(item[c])
						)}
					>
						{c === '처리상태' ? '검토중' : item[columnKeyMap[c]]}
					</span>
				</li>
			);
		});
	};

	const applyEventSupport = async () => {
		try {
			const token = localStorage.getItem('accessToken');

			const values = Object.values(applyFormInfo);
			console.log('applyFormInfo >> ', applyFormInfo);
			const hasEmpty = values.some((item) => {
				console.log(item);
				return !item || item == '';
			});
			if (hasEmpty || values.length == 0) {
				toast('필수 값이 누락되어 있습니다. 필수 값을 입력해주세요.');
				return;
			}

			const res = await baseApi.post(
				'/api/v1/support',
				{
					eventType: selectedEventType || '',
					familyRelation: applyFormInfo?.relation || '',
					targetName: applyFormInfo?.targetName || '',
					applicationDate: parsingDate(new Date()),
					eventDate: date,
					requestedAmount: 50000,
					eventLocation: applyFormInfo?.eventLocation,
					accountNumber: applyFormInfo?.bankNumber,
					bankName: applyFormInfo?.bankName,
					accountHolder: applyFormInfo?.holderName,
					approvalStatus: '확인',
					memo: '',
					...(uploadedFileId && { fileIdList: [uploadedFileId] }),
				},
				{
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);
			toast('경조비 신청 완료');
			getAppliedHistory();
			setApplyFormInfo({ ...initialApplyFormInfo });
		} catch (e) {
		} finally {
		}
	};

	return (
		<div className={c.container}>
			<BreadCrumb />
			<MainTitleWrapper
				mainTitleData={{
					title: '경조비신청',
					desc: '경조사 발생 시 경조비를 신청하고 지급 현황을 관리합니다.',
				}}
			/>

			<div className={c.formContainer}>
				<div className={c.formTitle}>
					<div className={c.formTitleLeft}>
						<HeartHandshake color="#1B3A6B" size={15} />
						<p>경조비신청 입력</p>
					</div>
					<div className={c.formTitleRight}>
						<span>*</span>
						<p>필수 입력 항목</p>
					</div>
				</div>

				<div className={c.formContent}>
					<section className={c.formItem}>
						<p className={c.formItemTitle}>신청자 정보</p>
						<div className={c.formItemData}>
							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>사원번호</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										readOnly
										className={c.formInput}
										disabled
										value={userInfo?.employeeNo}
									/>
									<Lock
										size={12}
										color="#9CA3AF"
										className="absolute right-[12px] top-1/2 -translate-y-1/2"
									/>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>성명</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										readOnly
										className={c.formInput}
										disabled
										value={userInfo?.name}
									/>
									<Lock
										size={12}
										color="#9CA3AF"
										className="absolute right-[12px] top-1/2 -translate-y-1/2"
									/>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>부서</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										readOnly
										className={c.formInput}
										disabled
										value={userInfo?.departmentName}
									/>
									<Lock
										size={12}
										color="#9CA3AF"
										className="absolute right-[12px] top-1/2 -translate-y-1/2"
									/>
								</div>
							</div>
							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>직급</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										readOnly
										className={c.formInput}
										disabled
										value={userInfo?.position}
									/>
									<Lock
										size={12}
										color="#9CA3AF"
										className="absolute right-[12px] top-1/2 -translate-y-1/2"
									/>
								</div>
							</div>
							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>신청일</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										readOnly
										className={c.formInput}
										disabled
										value={getToday()}
									/>
									<Lock
										size={12}
										color="#9CA3AF"
										className="absolute right-[12px] top-1/2 -translate-y-1/2"
									/>
								</div>
							</div>
						</div>
					</section>

					<section className={c.formItem}>
						<p className={c.formItemTitle}>
							경조 구분
							<span className="text-[#EF4444]">*</span>
						</p>
						<div className={c.formItemData}>
							<div className={c.eventTypeList}>
								{eventTypeList.map((item, idx) => (
									<>
										<div
											key={idx}
											className={clsx(
												c.eventTypeItem,
												item.text === selectedEventType && c.active
											)}
											onClick={() => setSelectedEventType(item.text)}
										>
											{item.icon}
											<span>{item.text}</span>
										</div>
									</>
								))}
							</div>
						</div>

						<span className={c.eventDesc}>
							<Info size={13} color="#2563EB" />
							<span>본인결혼 선택됨 · 지급기준액: 500,000원</span>
						</span>
					</section>

					<section className={c.formItem}>
						<p className={c.formItemTitle}>경조 대상자 정보</p>

						<div className={c.formItemData}>
							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>
									대상자성명
									<span className="text-[#EF4444]">*</span>
								</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										className={c.formInput2}
										value={applyFormInfo?.targetName}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												targetName: e.target.value,
											}))
										}
									/>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>
									관계
									<span className="text-[#EF4444]">*</span>
								</p>

								<div className={c.formInputWrapper}>
									<select
										className={c.formSelect2}
										value={applyFormInfo?.relation}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												relation: e.target.value,
											}))
										}
									>
										<option value="">선택하세요</option>
										{relationList.map((item, idx) => (
											<option key={idx} value={item.value}>
												{item.label}
											</option>
										))}
									</select>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>
									경조일
									<span className="text-[#EF4444]">*</span>
								</p>
								<Popover open={openCalendar} onOpenChange={setOpenCalendar}>
									<PopoverTrigger>
										<div className={c.triggerWrapper}>
											<span className={c.triggerDate}>{date}</span>
											<CalendarDays size={13} color="#9CA3AF" />
										</div>
									</PopoverTrigger>

									<PopoverContent>
										<Calendar
											mode="single"
											selected={date}
											onSelect={(date) => {
												setDate(parsingDate(date));
												setOpenCalendar(false);
											}}
										/>
									</PopoverContent>
								</Popover>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>경조장소</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="EMP-001"
										className={c.formInput2}
										value={applyFormInfo?.eventLocation}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												eventLocation: e.target.value,
											}))
										}
									/>
								</div>
							</div>
						</div>
					</section>

					<section className={c.formItem}>
						<p className={c.formItemTitle}>
							지급 계좌
							<span className="text-[#EF4444]">*</span>
						</p>
						<div className={c.formItemData}>
							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>은행명</p>
								<div className={c.formInputWrapper}>
									<select
										className={c.formSelect2}
										value={applyFormInfo?.bankName}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												bankName: e.target.value,
											}))
										}
									>
										<option value='"'>선택하세요</option>
										{bankList.map((item, idx) => (
											<option key={idx} value={item.label}>
												{item.label}
											</option>
										))}
									</select>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>계좌번호</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										placeholder="- 없이 숫자만 입력"
										className={c.formInput2}
										value={applyFormInfo?.bankNumber}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												bankNumber: e.target.value,
											}))
										}
									/>
								</div>
							</div>

							<div className={c.formApplyInfoItem}>
								<p className={c.formInputLabel}>예금주</p>
								<div className={c.formInputWrapper}>
									<input
										type="text"
										className={c.formInput2}
										value={applyFormInfo?.holderName}
										onChange={(e) =>
											setApplyFormInfo((prev) => ({
												...prev,
												holderName: e.target.value,
											}))
										}
									/>
								</div>
							</div>
						</div>
					</section>

					<section className={c.formItem}>
						<input
							type="file"
							ref={fileUploaderRef}
							accept=".jpg,.jpeg,.png,.pdf"
							onChange={(e) => {
								console.log('e', e.target.files);

								fileUpload(e.target.files);
							}}
							hidden
						/>
						<p className={c.formItemTitle}>
							첨부파일
							<span className="text-[#EF4444]">*</span>
						</p>

						<div className={c.formUploadSection}>
							{/* 파일업로드 클릭영역 */}
							<div className={c.formUploadWrapper}>
								<Paperclip size={13} color="#9CA3AF" />
								<div className={c.formUploadText}>
									<span className={c.textTop}>
										청첩장·출생증명서 등 관련 서류를 첨부해 주세요
									</span>
									<span className={c.textBottom}>
										PDF, JPG, PNG · 최대 10MB · 파일 1개
									</span>
								</div>
								<div>
									<CButton
										beforeIcon={<Download size={13} color="#374151" />}
										buttonName="파일선택"
										fontSize={13}
										padding="6px 16px"
										onClick={() => {
											if (uploadedFileList.length >= 1) {
												toast('1개만 등록이 가능합니다.');
												return;
											}
											fileUploaderRef?.current?.click();
										}}
									/>
								</div>
							</div>

							{/* 업로드된 리스트 */}
							{uploadedFileList.length > 0 &&
								uploadedFileList.map((item, idx) => (
									<>
										<div className={c.formUploadedFilesWrapper}>
											<div className={c.uploadInfoWrapper}>
												<FileText color="#3B82F6" size={15} />
												<div className={c.formUploadedInfo}>
													<span className={c.formUploadedFileName}>
														{item.fileName}
													</span>
													<span className={c.formUploadedFileSpec}>
														{item.fileSize} · 업로드 완료
													</span>
												</div>
											</div>
											<div
												className={c.uploadDeleteButton}
												onClick={() => setUploadedFileList([])}
											>
												<XIcon size={13} color="#EF4444" />
												<span>삭제</span>
											</div>
										</div>
									</>
								))}

							{/* 비고 영역 */}
							<div className={c.formUploadCommentWrapper}>
								<p className={c.commentTitle}>비고</p>
								<textarea
									name=""
									id=""
									className={c.commentTextArea}
									placeholder="추가 사항을 입력하세요. (선택)"
								></textarea>
							</div>
						</div>
					</section>
					{/* 버튼영역 */}

					<div className={c.uploadButtonWrapper}>
						<CButton
							buttonName="취소"
							beforeIcon={<XIcon size={13} color="#6B7280" />}
						/>
						<CButton
							buttonName="신청하기"
							beforeIcon={<SendHorizontal size={13} />}
							type="type2"
							onClick={() => applyEventSupport()}
						/>
					</div>
				</div>

				{/* 테이블영역 */}
				<ViewTable
					columns={columns}
					smallColumnIdxList={smallFlexIndex}
					renderRow={renderRow}
					rowList={rowList}
				/>
			</div>

			<WelfareDetailModal
				open={openDialog}
				setOpen={setOpenDialog}
				isLoading={isLoading}
				detailInfo={modalDetailInfo}
			/>
			<LoadingSpinner isLoading={isLoading} />
		</div>
	);
}
