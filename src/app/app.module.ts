import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WelcomeComponent } from './welcome/welcome.component';
import { NavComponent } from './nav/nav.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { ReactiveFormsModule } from '@angular/forms';
import { TermsComponent } from './terms/terms.component';  
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
// import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { AddTechnologyComponent } from './add-technology/add-technology.component';
import { TechnologiesComponent } from './technologies/technologies.component'; 
import { SubscriptionComponent } from './subscriptions/subscriptions.component';
import { BlogsComponent } from './blogs/blogs.component';
import { TechnologyService } from './technology.service';
import { SubscriptionService } from './subscriptions.service';
import { AuthInterceptor } from './Services/interceptor.service';
import { NotificationService } from './notification.service';
import { UpdateComponent } from './update/update.component';
import { UpdateService } from './update.service';
import { NotificationComponent } from './notification/notification.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { NavbarComponent } from './navbar/navbar.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { AdminDashboardComponent} from './admin-dahboard/admin-dashboard.component';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { AdminNavbarComponent } from './admin-navbar/admin-navbar.component';
import { AdminSidebarComponent } from './admin-sidebar/admin-sidebar.component';
import { AdminUsersComponent } from './admin-users/admin-users.component';
import { AdminTechComponent } from './admin-tech/admin-tech.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
import { PreviousUpdatesComponent } from './previous-updates/previous-updates.component';
import { EarlierUpdatesComponent } from './earlier-updates/earlier-updates.component';
import { SearchedTermComponent } from './searched-term/searched-term.component';

@NgModule({
  declarations: [
    AppComponent,
    WelcomeComponent,
    NavComponent,
    FooterComponent,
    LoginComponent,
    SignupComponent,
    AboutComponent,
    ContactComponent,
    TermsComponent,
    AdminDashboardComponent,
    HomeComponent,
    // ForgotPasswordComponent,
    ResetPasswordComponent,
    AddTechnologyComponent,
    TechnologiesComponent,
    SubscriptionComponent,
    BlogsComponent,
    UpdateComponent,
    NotificationComponent,
    SidebarComponent,
    NavbarComponent,
    UserDashboardComponent,
    AdminHomeComponent,
    AdminNavbarComponent,
    AdminSidebarComponent,
    AdminUsersComponent,
    AdminTechComponent,
    PreviousUpdatesComponent,
    EarlierUpdatesComponent,
    SearchedTermComponent,

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule ,// Add FormsModule here
    CommonModule,
    HttpClientModule,
    RouterModule,
    BrowserAnimationsModule,
    // ToastrModule.forRoot(),
  
  ],
  providers: [TechnologyService, SubscriptionService, NotificationService, UpdateService, 
    {provide:HTTP_INTERCEPTORS, useClass:AuthInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

