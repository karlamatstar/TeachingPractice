"use client";

import s from "./MainTitle.module.css";

const intialTitleData = {
	title: "인사정보등록",
	desc: "직원의 인사정보를 등록하고 관리합니다.",
};

// export default function MainTitleWrapper({mainTitleData, buttonRender}) {
export default function MainTitleWrapper({mainTitleData = {...intialTitleData}, buttonRender}) {
	
	return (
		<div className={s.container}>
			<div className={s.titleArea}>
				<span className={s.mainTitle}>{mainTitleData.title}</span>
				<span className={s.desc}>{mainTitleData.desc}</span>
			</div>
			
			<div className={s.buttonArea}>{buttonRender?.()}</div>
		
		</div>
	);
}
