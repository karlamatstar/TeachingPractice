'use client';

import BreadCrumb from '@/component/common/BreadCrumb';
import MainTitleWrapper from '@/component/common/MainTitleWrapper';
import SearchBar from '@/component/common/SearchBar';
import ViewTable from '@/component/common/ViewTable';
import CEditButton from '@/component/common/element/CEditButton';
import CStatusLabel from '@/component/common/element/CStatusLabel';
import { useEffect, useState } from 'react';
import baseApi from '@/common/api/baseApi';
import { clsx } from 'clsx';
import {
	Dialog,
	DialogContent,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from '@/components/ui/dialog';
import s from '@/component/common/MainTitle.module.css';
import { Save, UserPlus, XIcon } from 'lucide-react';
import CInput from '@/component/common/element/CInput';
import CSelect from '@/component/common/element/CSelect';
import PostCodeButton from '@/component/common/PostCodeButton';
import CButton from '@/component/common/element/CButton';
import { toast } from 'sonner';
import LoadingSpinner from '@/common/LoadingSpinner';
import ConfirmAlert from '@/common/ConfirmAlert';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const columns = [
	'NO',
	'사원번호',
	'성명',
	'부서',
	'직급',
	'입사일',
	'연락처',
	'이메일',
	'재직상태',
	'관리',
];

const columnKeyMap = {
	사원번호: 'employeeNo',
	성명: 'name',
	부서: 'departmentName',
	직급: 'positionName',
	입사일: 'hireDate',
	연락처: 'phone',
	이메일: 'email',
	재직상태: 'status',
};

export default function InfoRegister() {
	const [employees, setEmployees] = useState([]);
	const [selectedInfo, setSelectedInfo] = useState({});
	const [open, setOpen] = useState(false);
	const [registerInfo, setRegisterInfo] = useState({});
	const [isEdit, setIsEdit] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [isOpenAlert, setIsOpenAlert] = useState(false);

	const buttonRender = () => {
		return (
			<>
				<CButton
					path="/download.png"
					type="type1"
					buttonName="PDF 다운로드"
					onClick={() => {
						setIsOpenAlert(true);
					}}
				/>
				<CButton
					path="/plus.png"
					type="type2"
					buttonName="신규등록"
					onClick={() => {
						setSelectedInfo({});
						setIsEdit(false);
						setOpen(true);
					}}
				/>
			</>
		);
	};

	const renderCell = (row, column) => {
		if (column === 'NO') {
			return null;
		}

		if (column === '관리') {
			return (
				<CEditButton
					buttonName="수정"
					onClick={() => {
						setSelectedInfo(row);
						setOpen(true);
						setIsEdit(true);
					}}
				/>
			);
		}

		const key = columnKeyMap[column];

		if (key === 'status') {
			return (
				<CStatusLabel
					type={row[key] === '재직' ? 'type1' : 'type2'}
					labelName={row[key]}
				/>
			);
		}

		return row[key];
	};

	const getEmployees = async (params) => {
		try {
			setIsLoading(true);
			const token = localStorage.getItem('accessToken');
			const res = await baseApi.get('/api/v1/employees', {
				headers: {
					Authorization: `Bearer ${token}`,
				},
				params: { ...params },
			});

			setEmployees(res?.data?.data);
		} catch (e) {
			console.error(e.status);
		} finally {
			setIsLoading(false);
		}
	};

	const registerEmployee = async () => {
		const param = !isEdit
			? { ...registerInfo, employmentStatus: '재직중' }
			: { ...selectedInfo, employmentStatus: '재직중' };

		const token = localStorage.getItem('accessToken');
		try {
			setIsLoading(true);
			const url = '/api/v1/employees/registerEmployee';
			const res = await baseApi.post(
				url,
				{
					...param,
				},
				{ headers: { Authorization: `Bearer ${token}` } }
			);

			if (res?.data?.success) {
				toast(`사원${isEdit ? '수정' : '등록'}이 정상처리 되었습니다.`, {
					position: 'top-center',
				});
				setOpen(false);

				// 재조회
				getEmployees();
			}
		} catch (error) {
			toast(error?.response?.data?.message, { position: 'top-center' });
		} finally {
			setIsLoading(false);
		}
	};

	const fontToBase64 = async (fontPath) => {
		const res = await fetch(fontPath);
		const buffer = await res.arrayBuffer();

		let binary = '';
		const bytes = new Uint8Array(buffer);

		bytes.forEach((byte) => {
			binary += String.fromCharCode(byte);
		});

		return btoa(binary);
	};

	const downloadPdf = async () => {
		const doc = new jsPDF();

		const fontBase64 = await fontToBase64('/fonts/NotoSansKR-Regular.ttf');

		doc.addFileToVFS('NotoSansKR-Regular.ttf', fontBase64);
		doc.addFont('NotoSansKR-Regular.ttf', 'NotoSansKR', 'normal');

		doc.setFont('NotoSansKR', 'normal');

		const cols = columns.filter((item) => item !== '관리' && item !== 'NO');

		autoTable(doc, {
			head: [cols],
			// body: [
			//
			// 	["김지원", "IT본부", "과장"],
			// 	["리흔", "경영지원본부", "사원"],
			// ],
			body: employees.map((employee, idx) => {
				const test = cols.map((c) => employee[columnKeyMap[c]]);
				console.log('test', test);
				return [idx, ...cols.map((c) => employee[columnKeyMap[c]])];
			}),
			styles: {
				font: 'NotoSansKR',
				fontStyle: 'normal',
			},
		});

		doc.save('employee.pdf');
	};

	useEffect(() => {
		console.log('jsPDF >> ', jsPDF);
		getEmployees();
	}, []);

	return (
		<div className="flex flex-col gap-[16px]">
			<BreadCrumb />
			<MainTitleWrapper buttonRender={buttonRender} />
			<SearchBar goSearch={(params) => getEmployees(params)} />
			<ViewTable
				columns={columns}
				rowList={employees}
				smallColumnIdxList={[2, 4, 8, 9]}
				renderRow={(row, index) => (
					<>
						{columns.map((column, columnIndex) => {
							if (column === 'NO') {
								return <li key={`${column}-${columnIndex}`}>{index + 1}</li>;
							}

							return (
								<li
									key={`${column}-${columnIndex}`}
									className={clsx(
										[2, 4, 8, 9].includes(columnIndex) ? 'flex-[0.5]' : 'flex-1'
									)}
								>
									{renderCell(row, column)}
								</li>
							);
						})}
					</>
				)}
			/>

			<Dialog open={open} onOpenChange={setOpen}>
				<DialogContent
					showCloseButton={false}
					className={'w-[600px] max-w-none p-0'}
				>
					<DialogHeader className={clsx('bg-[#1B3A6B]', s.modalHeader)}>
						<DialogTitle>
							<div className={'flex items-center justify-between'}>
								<div className={'flex items-center gap-[10px]'}>
									<UserPlus color="#60A5FA" />
									<span className={'text-[16px] font-bold text-[#fff]'}>
										인사정보등록
									</span>
								</div>

								<div
									className={clsx('bg-[#2D5F9E]', s.closeBtn, 'cursor-pointer')}
									onClick={() => setOpen(false)}
								>
									<XIcon size={16} color="#fff" />
								</div>
							</div>
						</DialogTitle>
					</DialogHeader>
					<div className={s.modalContent}>
						<div className={s.contentItem}>
							<p className={s.title}>기본정보</p>
							<section className={s.formSection}>
								<div className={s.formItem}>
									<label htmlFor="">
										사원번호
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										readOnly
										disabled
										value={selectedInfo?.employeeNo}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">
										성명
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										value={
											selectedInfo?.name
												? selectedInfo?.name
												: registerInfo?.name
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												name: e.target.value,
											}))
										}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">
										부서
										<span className="text-[#EF4444]">*</span>
									</label>
									<CSelect
										width={268}
										value={
											selectedInfo?.departmentName
												? selectedInfo?.departmentName
												: registerInfo?.departmentName
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												departmentName: e.target.value,
											}))
										}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">
										직급
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										value={
											selectedInfo?.positionName
												? selectedInfo?.positionName
												: registerInfo?.positionName
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												positionName: e.target.value,
											}))
										}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">
										입사일
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										value={
											selectedInfo?.hireDate
												? selectedInfo?.hireDate
												: registerInfo?.hireDate
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												hireDate: e.target.value,
											}))
										}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">
										재직상태
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										value={selectedInfo?.status || '재직중'}
										disabled
										readOnly
									/>
								</div>
							</section>
						</div>

						{/*연락처 영역*/}
						<div className={s.contentItem}>
							<p className={s.title}>연락처</p>
							<section className={s.formSection}>
								<div className={s.formItem}>
									<label htmlFor="">
										휴대폰
										<span className="text-[#EF4444]">*</span>
									</label>
									<CInput
										width={268}
										value={
											selectedInfo?.phone
												? selectedInfo?.phone
												: registerInfo?.phone
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												phone: e.target.value,
											}))
										}
									/>
								</div>

								<div className={s.formItem}>
									<label htmlFor="">이메일</label>
									<CInput
										width={268}
										value={
											selectedInfo?.email
												? selectedInfo?.email
												: registerInfo?.email
										}
										onChange={(e) =>
											setRegisterInfo((prev) => ({
												...prev,
												email: e.target.value,
											}))
										}
									/>
								</div>
							</section>
						</div>

						{/*주소영역*/}
						<div className={s.contentItem}>
							<p className={s.title}>주소</p>
							<section className={s.formSection}>
								<div className={clsx(s.formItem, s.postItem)}>
									<label htmlFor="">우편번호</label>
									<div className="flex gap-[8px]">
										<CInput
											width={160}
											readOnly
											disabled
											value={
												selectedInfo?.postCode
													? selectedInfo?.postCode
													: registerInfo?.postCode
											}
										/>
										<PostCodeButton
											onCompletePostData={(data) => {
												const roadAddress = data?.roadAddress;
												const zoneCode = data?.zonecode;
												if (isEdit) {
													setSelectedInfo((prev) => ({
														...prev,
														postCode: zoneCode,
														address: roadAddress,
													}));
												} else {
													setRegisterInfo((prev) => ({
														...prev,
														postCode: zoneCode,
														address: roadAddress,
													}));
												}
											}}
										/>
									</div>
								</div>

								<div className={clsx(s.formItem, s.postItem)}>
									<label htmlFor="">도로명주소</label>
									<CInput
										width={568}
										readOnly
										disabled
										value={
											isEdit ? selectedInfo?.address : registerInfo?.address
										}
									/>
								</div>

								<div className={clsx(s.formItem, s.postItem)}>
									<label htmlFor="">상세주소</label>
									<CInput
										width={568}
										value={
											isEdit
												? selectedInfo?.detailedAddress
												: registerInfo?.detailedAddress
										}
										onChange={(e) => {
											if (isEdit) {
												setSelectedInfo((prev) => ({
													...prev,
													detailedAddress: e.target.value,
												}));
											} else {
												setRegisterInfo((prev) => ({
													...prev,
													detailedAddress: e.target.value,
												}));
											}
										}}
									/>
								</div>
							</section>
						</div>

						{/*비상연락처*/}
						<div className={s.contentItem}>
							<p className={s.title}>비상연락처</p>
							<section className={clsx(s.formSection, s.emergency)}>
								<div className={clsx(s.formItem)}>
									<label htmlFor="">성명</label>
									<CInput width={174} />
								</div>

								<div className={clsx(s.formItem)}>
									<label htmlFor="">관계</label>
									<CSelect width={140} />
								</div>

								<div className={clsx(s.formItem)}>
									<label htmlFor="">연락처</label>
									<CInput width={174} />
								</div>
							</section>
						</div>
					</div>

					<DialogFooter>
						<div className={s.footerContainer}>
							<span className={s.footerGuide}>
								<span className="text-[#EF4444] mr-[5px]">*</span>
								필수 입력 항목입니다.
							</span>

							<div className={s.footerButtons}>
								<CButton
									buttonName="취소"
									beforeIcon={<XIcon size={14} />}
									onClick={() => setOpen(false)}
								/>
								<CButton
									type="type2"
									buttonName="저장"
									beforeIcon={<Save size={14} />}
									onClick={() => {
										console.log('regieterInfo ', registerInfo);
										registerEmployee();
									}}
								/>
							</div>
						</div>
					</DialogFooter>
					<LoadingSpinner isLoading={isLoading} />
				</DialogContent>
			</Dialog>

			<LoadingSpinner isLoading={isLoading} />
			<ConfirmAlert
				isOpen={isOpenAlert}
				setOpen={setIsOpenAlert}
				message="PDF를 다운 받으시겠습니까?"
				clickOk={downloadPdf}
			/>
		</div>
	);
}
