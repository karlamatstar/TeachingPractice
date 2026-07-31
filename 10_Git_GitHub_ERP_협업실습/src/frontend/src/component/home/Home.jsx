'use client';

import c from '@/component/home/Home.module.css';
import Nav from '@/component/common/Nav';
import {
	BanknoteArrowUp,
	Briefcase,
	Building2,
	CircleCheck,
	Clock,
	Eye,
	EyeOff,
	IdCard,
	Info,
	Lock,
	LogIn,
	Mail,
	ShieldCheck,
	UserPen,
	Users,
} from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import CInputCustom from '@/component/common/element/CInputCustom';
import { useEffect, useState } from 'react';
import baseApi from '@/common/api/baseApi';
import { useRouter } from 'next/navigation';

export default function Home() {
	const [loginUserInfo, setLoginUserInfo] = useState({});
	const [keepLogin, setKeepLogin] = useState(false);

	const router = useRouter();

	const goLogin = async (params) => {
		try {
			const res = await baseApi.post('/api/v1/employees/login', {
				...(params || loginUserInfo),
			});

			if (res.data.data.accessToken) {
				if (keepLogin) {
					localStorage.setItem('keepLogin', 'true');
					localStorage.setItem('loginInfo', JSON.stringify(loginUserInfo));
				}

				localStorage.setItem('accessToken', res.data.data.accessToken);
				localStorage.setItem('user', JSON.stringify(res.data.data));
				router.push('/info/register');
				return;
			}

			alert('로그인 실패');
		} catch (e) {
			alert('네트워크 통신에 실패하였습니다.');
		}
	};

	useEffect(() => {
		const keepLogin = localStorage.getItem('keepLogin');
		const loginInfo = localStorage.getItem('loginInfo');
		console.log('loginInfo >> ', loginInfo);
		if (keepLogin === 'true' && loginInfo) {
			const savedLoginInfo = JSON.parse(loginInfo);
			console.log(savedLoginInfo);

			goLogin(savedLoginInfo);
		}
	}, []);

	const renderJoin = () => {
		return (
			<div className={`${c.joinArea} ${c.stagger}`}>
				<div className={c.joinWrapper}>
					<section className={c.titleSection}>
						<p>회원가입</p>
						<span>계정을 만들어 인사관리를 시작하세요</span>
					</section>

					<section className={c.joinFormSection}>
						<CInputCustom labelName="성" placeholder="성" />

						<CInputCustom labelName="이름" placeholder="이름" />

						<CInputCustom
							beforeIcon={<IdCard color="#9CA3AF" />}
							labelName="사번"
							placeholder="EMP-001"
						/>

						<CInputCustom
							beforeIcon={<Building2 color="#9CA3AF" />}
							labelName="부서"
							placeholder="소속 부서 선택"
						/>

						<CInputCustom
							beforeIcon={<Briefcase color="#9CA3AF" />}
							labelName="직급"
							placeholder="직급선택"
						/>

						<CInputCustom
							beforeIcon={<Mail color="#9CA3AF" />}
							labelName="회사 이메일"
							placeholder="company@example.com"
						/>

						<CInputCustom
							beforeIcon={<Lock color="#9CA3AF" />}
							labelName="비밀번호"
							placeholder="비밀번호 입력"
							afterIcon={<Eye color="#9CA3AF" />}
						/>

						<CInputCustom
							beforeIcon={<Lock color="#9CA3AF" />}
							labelName="비밀번호 확인"
							placeholder="비밀번호 재입력"
							afterIcon={<CircleCheck color="#5da1f8" />}
						/>
					</section>

					<section className={c.guideAndConsent}>
						<div className={c.guideContentWrapper}>
							<Info size={11} color="#9CA3AF" />
							<span className={c.guideContent}>
								영문, 숫자, 특수문자 포함 8자리 이상
							</span>
						</div>

						<div className={c.consentWrapper}>
							<div className={c.checkConsent}>
								<Checkbox checked={true} />
								<Checkbox checked={true} />
								<span>이용약관 및 개인정보처리방침에 동의합니다</span>
							</div>
							<span className={c.consentClickButton}>내용 보기</span>
						</div>
					</section>

					<section className={c.joinButtonSection}>
						<div className={c.joinButton}>
							<UserPen size={18} color="#FFFFFF" />
							<UserPen size={18} color="#FFFFFF" />
							<span>회원가입</span>
						</div>

						<div className={c.loginButton}>
							<p>
								이미 계정이 있으신가요?
								<span>로그인하기</span>
							</p>
						</div>
					</section>
				</div>
			</div>
		);
	};

	const renderLogin = () => {
		return (
			<div className={`${c.loginArea} ${c.stagger}`}>
				<section className={c.titleSection}>
					<p>로그인</p>
					<span>계정에 로그인하여 업무를 시작하세요</span>
				</section>

				<section className={c.inputSection}>
					<div className={c.inputItem}>
						<Mail className={c.mail} color="#9CA3AF" />
						<Mail className={c.mail} color="#9CA3AF" />
						<label htmlFor="email">이메일</label>
						<input
							type="text"
							placeholder="이메일 주소를 입력하세요"
							onChange={(e) =>
								setLoginUserInfo((prev) => ({ ...prev, email: e.target.value }))
							}
						/>
					</div>

					<div className={c.inputItem}>
						<Lock className={c.mail} color="#9CA3AF" />
						<Lock className={c.mail} color="#9CA3AF" />
						<label htmlFor="email">비밀번호</label>
						<input
							type="password"
							placeholder="비밀번호를 입력하세요"
							onChange={(e) =>
								setLoginUserInfo((prev) => ({
									...prev,
									password: e.target.value,
								}))
							}
							onKeyDown={(e) => {
								if (e.key === 'Enter') {
									goLogin();
								}
							}}
						/>
						<EyeOff className={c.eye} color="#9CA3AF" />
						<EyeOff className={c.eye} color="#9CA3AF" />
						{/*<Eye className={c.mail} color='#9CA3AF'/>*/}
					</div>
				</section>

				<section className={c.loginOptionSection}>
					<div className={c.loginOptionItem}>
						<Checkbox onClick={() => setKeepLogin(!keepLogin)} />
						<span className={c.keepLoginTitle}>로그인 상태 유지</span>
					</div>

					<div className={c.loginOptionItem}>
						<span className={c.findPw}>비밀번호 찾기</span>
					</div>
				</section>

				<section className={c.loginButtonSection}>
					<div className={c.loginButtonItem} onClick={() => goLogin()}>
						<LogIn />
						<span>로그인</span>
					</div>

					<div className={c.loginButtonOr}>
						<span>또는</span>
					</div>

					<div>
						<img src="kakaologin.png" alt="" className="w-[400px] h-[60px]" />
					</div>
				</section>

				<section className={c.joinSection}>
					<div className={c.joinItem}>
						<span className={c.noAccount}>계정이 없으신가요?</span>
						<span className={c.applyJoin}>회원가입 신청</span>
					</div>
				</section>
			</div>
		);
	};

	return (
		<div className={c.container}>
			<Nav />

			<div className={c.loginContentWrapper}>
				<div className={`${c.guideArea} ${c.stagger}`}>
					<p className={c.guideTitle}>
						<ShieldCheck />
						<ShieldCheck />
						<span>Enterprise HR Solution</span>
					</p>

					<p className={c.guideCenterTitle}>
						스마트한 인사관리의 <br />
						스마트한 인사관리의 <br />
						<span className={c.centerTitleHL}>새로운 기준</span>
					</p>

					<p className={c.guideDesc}>
						직원 채용부터 급여, 근태까지 <br />
						직원 채용부터 급여, 근태까지 <br />
						하나의 플랫폼으로 관리하세요
					</p>

					<ul className={c.spec}>
						<li>
							<span className={c.specNumber}>2,400+</span>
							<span className={c.specDesc}>기업도입</span>
						</li>
						<li>
							<span className={c.specNumber}>98%</span>
							<span className={c.specDesc}>고객 만족도</span>
						</li>
						<li>
							<span className={c.specNumber}>15년</span>
							<span className={c.specDesc}>서비스 운영</span>
						</li>
					</ul>

					<ul className={c.functionList}>
						<li>
							<span className={c.functionIcon}>
								<Users color="#60A5FA" />
							</span>

							<div>
								<p className={c.functionTitle}>인사관리</p>
								<span className={c.functionDesc}>
									조직도, 인사발령, 직원 정보 통합 관리
								</span>
							</div>
						</li>

						<li>
							<span className={c.functionIcon}>
								<BanknoteArrowUp color="#60A5FA" />
							</span>

							<div>
								<p className={c.functionTitle}>급여관리</p>
								<span className={c.functionDesc}>
									자동 급여 계산, 세금 신고, 명세서 발송
								</span>
							</div>
						</li>

						<li>
							<span className={c.functionIcon}>
								<Clock color="#60A5FA" />
							</span>

							<div>
								<p className={c.functionTitle}>근태관리</p>
								<span className={c.functionDesc}>
									출퇴근, 휴가, 초과근무 실시간 모니터링
								</span>
							</div>
						</li>
					</ul>
				</div>

				{renderLogin()}
				{/*{renderJoin()}*/}
			</div>
		</div>
	);
}
