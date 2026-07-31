'use client'

import c from './AppointMent.module.css';

import {Clock} from "lucide-react";

import BreadCrumb from "@/component/common/BreadCrumb";
import MainTitleWrapper from "@/component/common/MainTitleWrapper";
import SearchBar from "@/component/common/SearchBar";
import AppointmentForm from "@/component/appointment/AppointmentForm";
import ViewTable from "@/component/common/ViewTable";
import CButton from "@/component/common/element/CButton";
import {useState} from "react";
import {clsx} from "clsx";

const columns = [
		'NO',
		'발령번호',
		'사원번호',
		'성명',
		'발령유형',
		'전부서/직급',
		'후부서/직급',
		'발령일',
		'등록자',
		'관리'
];

const rowList = [
		{
				발령번호: 'APT-2025-003',
				사원번호: 'EMP-002',
				성명: '이영희',
				발령유형: '승진',

				'전부서': '경영지원팀',
				'전직급': '과장',
				'후부서': '경영지원팀',
				'후직급': '부장',

				발령일: '2025.07.01',
				등록자: '홍길동',
		},

		{
				발령번호: 'APT-2025-002',
				사원번호: 'EMP-001',
				성명: '김철수',
				발령유형: '전보',

				'전부서': '경영지원팀',
				'전직급': '과장',
				'후부서': '경영지원팀',
				'후직급': '부장',

				발령일: '2025.04.01',
				등록자: '홍길동',
		},

		{
				발령번호: 'APT-2025-001',
				사원번호: 'EMP-004',
				성명: '최지영',
				발령유형: '겸직',

				'전부서': '경영지원팀',
				'전직급': '과장',
				'후부서': '경영지원팀',
				'후직급': '부장',

				발령일: '2025.01.15',
				등록자: '홍길동',
		},
];

const renderCell = (row, column) => {
		if (column === 'NO') {
				return null;
		}

		if (column === '관리') {
				return (
						<li className="flex gap-[10px] flex-1 justify-center items-center">
								<button className='rounded-[4px] bg-[#EFF6FF] text-[12px] text-[#2563EB] px-2.5 py-1'>
										수정
								</button>
								<button className='ml-[4px] rounded-[4px] bg-[#FFF1F2] text-[12px] text-[#E11D48] px-2.5 py-1'>
										삭제
								</button>
						</li>
				)
		}

		const getAppointmentTypeColor = (type) => {
				switch (type) {
						case '승진':
								return c.type1;
						case '전보':
								return c.type2;
						case '겸직':
								return c.type3;
				}
		}

		return (
				<li
						className={
								clsx(
										column === "성명" && "font-bold",
										"flex-1 flex items-center justify-center",
										column === "발령유형" && c.tableAppointmentType,
										["전부서", "후부서", "전직급", "후직급"].includes(column) && 'flex flex-col'
								)
						}
				>
			<span
					className={clsx(getAppointmentTypeColor(row[column]))}
			>
				{
						["전부서/직급", "후부서/직급"].includes(column)
								? (
										<>
												<div>
														{
																column.includes("전부서")
																		? (
																				<div className="flex flex-col">
																						<span>{row.전부서}</span>
																						<span>{row.전직급}</span>
																				</div>
																		) : (
																				<div className="flex flex-col">
																						<span>{row.후부서}</span>
																						<span>{row.후직급}</span>
																				</div>
																		)
														}
												</div>
										</>
								) : (
										<>
												{row[column]}
										</>
								)
				}
			
			</span>
				</li>
		)
}

export default function AppointMent() {

		const [isShowForm, setIsShowForm] = useState(false);
		const [selectedRowIdx, setSelectedRowIdx] = useState(0);


		const buttonRender = () => {
				return (
						<>
								<CButton path="/download.png" type="type1" buttonName="PDF 다운로드" onClick={() => {
										// setIsOpenAlert(true);
								}}/>
								<CButton path="/plus.png" type="type2" buttonName="발령등록" onClick={() => {
										// setSelectedInfo({});
										// setIsEdit(false);
										// setOpen(true)
										setIsShowForm(true);
								}}/>
						</>
				);
		};

		return (
				<div className={c.container}>
						<BreadCrumb/>

						<MainTitleWrapper
								buttonRender={buttonRender}
						/>

						<SearchBar/>

						{isShowForm && (
								<AppointmentForm
										setIsShowForm={setIsShowForm}
								/>
						)}

						<ViewTable
								rowList={rowList}
								selectedRowIdx={selectedRowIdx}
								setSelectedRowIdx={setSelectedRowIdx}
								renderTitle={() => (
										<>
												<Clock
														color="#1B3A6B"
														size={15}
												/>

												<span className="text-[#1B3A6B] text-[14px] font-[700]">
              발령 이력
            </span>
										</>
								)}
								columns={columns}
								renderRow={(row, index) => {
										return (
												<>
														<li className="flex items-center justify-center">{index + 1}</li>
														{columns.map((column, columnIndex) => (
																renderCell(row, column)
														))}
												</>
										)
								}}


						/>
				</div>
		);
}