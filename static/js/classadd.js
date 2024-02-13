document.addEventListener('DOMContentLoaded', () => {
    const bar = document.querySelector('#bar-b');
    const over = document.querySelector('#over');
    const oover = document.querySelector('#oover');

    const profile = document.querySelector('.profile');
    const prof = document.querySelector('.prof');
    const con = document.querySelector('#con');
    const pro = document.querySelector('.pro');
    const pro2 = document.querySelector('.pro2');
    const pro3 = document.querySelector('.pro3');
    const pro4 = document.querySelector('.pro4');
    const pro5 = document.querySelector('.pro5');
    const pro6 = document.querySelector('.pro6');
    const pro7 = document.querySelector('.pro7');
    const pro8 = document.querySelector('.pro8');


    const probox = document.querySelector('.box');
    const probox2 = document.querySelector('.box2');
    const probox3 = document.querySelector('.box3');
    const probox4 = document.querySelector('.box4');
    const probox5 = document.querySelector('.box5');
    const probox6 = document.querySelector('.box6');
    const probox7 = document.querySelector('.box7');
    const probox8 = document.querySelector('.box8');



    bar.addEventListener('click', () => {
        con.classList.toggle('open');
        prof.classList.remove('open');

    });
    profile.addEventListener('click', () => {
        prof.classList.toggle('open')
        con.classList.remove('open');

    });
    oover.addEventListener('click', () => {
        con.classList.remove('open');
        prof.classList.remove('open');
    });

    over.addEventListener('click', () => {
        con.classList.remove('open');
        prof.classList.remove('open');
    });
    probox.addEventListener('mouseover', () => {
        pro.classList.add('show');
    });
    probox.addEventListener('mouseout', () => {
        pro.classList.remove('show');
    });
    probox2.addEventListener('mouseover', () => {
        pro2.classList.add('show');
    });
    probox2.addEventListener('mouseout', () => {
        pro2.classList.remove('show');
    });
    probox3.addEventListener('mouseover', () => {
        pro3.classList.add('show');
    });
    probox3.addEventListener('mouseout', () => {
        pro3.classList.remove('show');
    });
    probox4.addEventListener('mouseover', () => {
        pro4.classList.add('show');
    });
    probox4.addEventListener('mouseout', () => {
        pro4.classList.remove('show');
    });
    probox5.addEventListener('mouseover', () => {
        pro5.classList.add('show');
    });
    probox5.addEventListener('mouseout', () => {
        pro5.classList.remove('show');
    });
    probox6.addEventListener('mouseover', () => {
        pro6.classList.add('show');
    });
    probox6.addEventListener('mouseout', () => {
        pro6.classList.remove('show');
    });
    probox7.addEventListener('mouseover', () => {
        pro7.classList.add('show');
    });
    probox7.addEventListener('mouseout', () => {
        pro7.classList.remove('show');
    });
    probox8.addEventListener('mouseover', () => {
        pro8.classList.add('show');
    });
    probox8.addEventListener('mouseout', () => {
        pro8.classList.remove('show');
    });
})